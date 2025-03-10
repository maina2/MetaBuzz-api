from django.urls import path
from .views import ConversationListCreateView, MessageListCreateView

urlpatterns = [
    path("conversations/", ConversationListCreateView.as_view(), name="conversation-list-create"),
    path("messages/<int:conversation_id>/", MessageListCreateView.as_view(), name="message-list-create"),
]
