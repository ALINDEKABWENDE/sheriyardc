# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.room_name = f"chat_{min(self.user.username, self.other_username)}_{max(self.user.username, self.other_username)}"
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.user
        recipient = await self.get_user(self.other_username)

        await self.save_message(sender, recipient, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def save_message(self, sender, recipient, message):
        return Message.objects.create(sender=sender, recipient=recipient, content=message)

    @database_sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)
