from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from groq import Groq
import os
from django.shortcuts import render

def chat_page(request):
    return render(request, "chat_ai/chat.html")

class ChatAIViewSet(ViewSet):
    def create(self, request):
        message = request.data.get("message", "")

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=200,
            )

            reply = chat_completion.choices[0].message["content"]
        except Exception as e:
            reply = f"Error: {str(e)}"

        return Response({"reply": reply})
