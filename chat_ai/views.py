from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import render
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def chat_page(request):
    return render(request, "chat_ai/chat.html")


class ChatAIViewSet(ViewSet):
    def create(self, request):
        message = request.data.get("message", "")

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")

            response = model.generate_content(
                [
                    {"role": "system", "parts": [{"text": "You are a helpful AI assistant."}]},
                    {"role": "user", "parts": [{"text": message}]}
                ]
            )

            reply = response.text

        except Exception as e:
            reply = f"Error: {str(e)}"

        return Response({"reply": reply})
