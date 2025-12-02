import json
import os
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from groq import Groq
from asgiref.sync import sync_to_async


@sync_to_async
def get_flights():
    from flights.models import Flight
    flights = Flight.objects.select_related("departure_airport", "arrival_airport", "airplane").all()

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
        await self.send(json.dumps({"sender": "ai", "message": "Привіт! Мене звати Василій, я твій віртуальний помічник."}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_msg = data.get("message")

        await self.send(json.dumps({"sender": "user", "message": user_msg}))

        answer = await self.ask_groq(user_msg)

        await self.send(json.dumps({"sender": "ai", "message": answer}))

    async def ask_groq(self, prompt: str):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            loop = asyncio.get_event_loop()

            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                )
            )

            msg = response.choices[0].message.content

            try:
                data = json.loads(msg)
                if data.get("action") == "get_flights":
                    flights = await get_flights()
                    
                    return json.dumps(flights, ensure_ascii=False)
            except:
                pass

            return msg

        except Exception as e:
            return f"Error: {str(e)}"
