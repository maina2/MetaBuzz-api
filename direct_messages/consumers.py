import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message, Conversation

def get_user():
    return get_user_model()  # Ensure Django is initialized before accessing the User model

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.conversation_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        sender_id = data["sender_id"]
        text = data["text"]

        User = get_user()  # Fetch the User model inside the method
        sender = await User.objects.aget(id=sender_id)
        conversation = await Conversation.objects.aget(id=self.conversation_id)

        message = await Message.objects.acreate(sender=sender, conversation=conversation, text=text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender_username": sender.username,
                "text": message.text,
                "created_at": str(message.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
