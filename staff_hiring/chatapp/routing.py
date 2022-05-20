from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws//', consumers.ChatConsumer.as_asgi()), # Using asgi
]
print(websocket_urlpatterns,"fffffffffffffffffff")