import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from notifications.models import Notification
from asgiref.sync import sync_to_async
from .serializers import NotificationSerializer

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user = self.scope["user"]
        self.room_group_name = f"notifications_{self.user.id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        # Save notification to the database
        notification = await sync_to_async(Notification.objects.create)(
            user=self.user,
            message=message
        )

        serialized_notification = NotificationSerializer(notification).data

        # Send notification to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "notification": serialized_notification,
            }
        )

    async def send_notification(self, event):
        notification = event["notification"]
        await self.send(text_data=json.dumps(notification))
