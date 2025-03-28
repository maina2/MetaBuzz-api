from rest_framework import serializers
from .models import Message, Conversation
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender", "sender_username", "text", "created_at"]

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)  # updated here

    class Meta:
        model = Conversation
        fields = ["id", "participants", "messages", "created_at"]
