# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from asgiref.sync import sync_to_async
from .models import Message, Room
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room = text_data_json["room"]

        await self.save_message(message, username, room)

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message,
                "username": username,
                "room": room
            }
        )

        # Receive message from room group

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room = event["room"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                "message": message,
                "username": username,
                "room": room
            }
        ))

    @sync_to_async
    def save_message(self, message, username, room):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        Message.objects.create(
            user=user,
            room=room,
            content=message
        )

# import json

# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_router']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
