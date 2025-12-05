from django.urls import path
from .consumers import ChatAIConsumer

websocket_urlpatterns = [
    path("ws/chat/", ChatAIConsumer.as_asgi()),
]
