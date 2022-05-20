import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later
from .models import  Message, RoomCreate

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    
   
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name
    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
      
    )
    await self.accept()

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
  )

  async def receive(self, text_data):
    data = json.loads(text_data)
    
    message = data['message']
    sender_id=data['sender']
    reciever=data['reciever']
    room=self.room_name
    print(room,'-88888888888888888*********')
    
    await self.save_message(room, message,sender_id,reciever)
    print('its employe message-----------')
  # Send message to room group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'content': message,
        'send_id':sender_id,
        'reciever_id':reciever,
        'room':room
      }
    )
   
# # Receive message from room group
  async def chat_message(self, event):
    message = event['content']
    sender_id=event['send_id']
    reciever=event['reciever_id']
    room=event['room']

  # Send message to WebSocket
    await self.send(text_data=json.dumps({
    'content': message,
    'send_id':sender_id,
    'reciever_id':reciever,
    'room':room

    
     }))
    
  @sync_to_async
  def save_message(self, room, message, sender_id,reciever):
    print('mohit mdfdfl000000000',room)
    obj=RoomCreate.objects.get(room_name=room)

    msg=message.strip()
    print(msg)
    if msg:
      obj1=Message.objects.create(room=obj, content=message,send_id_id=sender_id,reciever_id_id=reciever)
      obj1.save()
    else:
      pass