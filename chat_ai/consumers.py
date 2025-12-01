import json
from channels.generic.websocket import AsyncWebsocketConsumer
from groq import Groq
import os
import asyncio

class ChatAIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"sender": "ai", "message": "Привіт! Я тут."}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get("message")

        await self.send(json.dumps({"sender": "user", "message": user_message}))

        reply = await self.ask_groq(user_message)

        await self.send(json.dumps({"sender": "ai", "message": reply}))

    async def ask_groq(self, prompt: str):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            loop = asyncio.get_event_loop()

            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": prompt}
                    ]
                )
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"
