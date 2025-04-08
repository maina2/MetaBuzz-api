from rest_framework import generics
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer,UserSerializer
from rest_framework import serializers  # Add this import
from rest_framework.response import Response
from django.db.models import Q



User = get_user_model()

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        participants = serializer.validated_data.get("participants")
        existing_conversation = Conversation.objects.filter(participants=self.request.user).filter(participants__in=participants).distinct()

        if existing_conversation.exists():
            raise serializers.ValidationError("A conversation with these participants already exists.")

        serializer.save()


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class StartConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if other_user == request.user:
            return Response({"error": "You cannot start a conversation with yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a conversation already exists with both participants
        existing = Conversation.objects.filter(participants=request.user)\
            .filter(participants=other_user).first()

        if existing:
            serializer = ConversationSerializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Otherwise, create a new conversation
        conversation = Conversation.objects.create()
        conversation.participants.set([request.user, other_user])
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class ConversationWithUserView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs["user_id"]
        # Get conversations where both the current user and the specified user are participants
        return Conversation.objects.filter(
            participants=self.request.user
        ).filter(
            participants__id=other_user_id
        )
    
class GlobalSearchView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "")
        if not query:
            return Response({"error": "Search query is required"}, status=400)

        # Search Users
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
        user_data = UserSerializer(users, many=True).data

        # Search Conversations
        conversations = Conversation.objects.filter(participants__username__icontains=query)
        conversation_data = ConversationSerializer(conversations, many=True).data

        # Search Messages (Use `text` instead of `content`)
        messages = Message.objects.filter(Q(text__icontains=query))
        message_data = MessageSerializer(messages, many=True).data

        return Response({
            "users": user_data,
            "conversations": conversation_data,
            "messages": message_data,
        })