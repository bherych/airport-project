import json
import os
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from google.generativeai import GenerativeModel
from asgiref.sync import sync_to_async
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@sync_to_async
def get_flights(params):
    from flights.models import Flight
    flights = Flight.objects.select_related(
        "departure_airport", "arrival_airport", "airplane"
    )

    status = params.get("status")
    if status:
        flights = flights.filter(status=status)

    date = params.get("date")
    if date:
        flights = flights.filter(departure_time__date=date)


    departure_city = params.get("departure_city")
    if departure_city:
        flights = flights.filter(departure_airport__name__icontains=departure_city)

    arrival_city = params.get("arrival_city")
    if arrival_city:
        flights = flights.filter(arrival_airport__name__icontains=arrival_city)

    data = []
    for f in flights:
        data.append({
            "flight_number": f.flight_number,
            "departure_airport": f.departure_airport.name,
            "arrival_airport": f.arrival_airport.name,
            "departure_time": f.departure_time.isoformat(),
            "arrival_time": f.arrival_time.isoformat(),
            "airplane": f.airplane.model if f.airplane else None,
            "status": f.status,
            "price": float(f.price) if f.price is not None else None,
        })
    return data



def load_system_prompt():
    path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class ChatAIConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.system_prompt = load_system_prompt()
        await self.accept()
        await self.send(json.dumps({"sender": "ai", "message": "Hello! My name is Vasyl. I'm your virtual assistant."}))

        self.model = GenerativeModel(
            model_name="gemini-2.5-flash",
            tools = [
                {
                    "function_declarations": [
                        {
                            "name": "get_flights",
                            "description": "Get flights with optional filters",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "date": {"type": "string"},
                                    "departure_city": {"type": "string"},
                                    "arrival_city": {"type": "string"},
                                    "status": {
                                        "type": "string",
                                        "enum": ["scheduled", "cancelled"]
                                    }
                                }
                            }
                        }
                    ]
                }
            ],
            system_instruction=self.system_prompt
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_msg = data.get("message")

        await self.send(json.dumps({"sender": "user", "message": user_msg}))

        answer = await self.ask_gemini(user_msg)

        await self.send(json.dumps({"sender": "ai", "message": answer}))


    async def ask_gemini(self, prompt: str):
        try:
            loop = asyncio.get_event_loop()

            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )

            try:
                if response.candidates:
                    parts = response.candidates[0].content.parts
                    for p in parts:
                        if hasattr(p, "function_call") and p.function_call:
                            fn = p.function_call
                            args = dict(fn.args) if fn.args else {}

                            if fn.name == "get_flights":
                                flights = await get_flights(args)

                                final = await loop.run_in_executor(
                                    None,
                                    lambda: self.model.generate_content(
                                        f"Here is the flight data:\n"
                                        f"{json.dumps(flights, ensure_ascii=False)}\n"
                                        f"Respond naturally."
                                    )
                                )

                                return final.text or "No response from model."
            except Exception as inner_err:
                return f"Function error: {inner_err}"

            return response.text or "No response."

        except Exception as e:
            return f"Error: {str(e)}"
