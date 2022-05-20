from urllib import request
from django.urls import path,re_path
from django.conf.urls import url


from . import consumers


websocket_urlpatterns = [
  re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()), # Using asgi
  # url(r'/ws/chat/', consumers.ChatConsumer.as_asgi())

]

