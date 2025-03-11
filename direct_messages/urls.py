from django.urls import path
from .views import ConversationListCreateView, MessageListCreateView,ConversationWithUserView,GlobalSearchView

urlpatterns = [
    path("conversations/with/<int:user_id>/", ConversationWithUserView.as_view(), name="conversation-with-user"),
    path("conversations/", ConversationListCreateView.as_view(), name="conversation-list-create"),
    path("conversations/<int:conversation_id>/messages/", MessageListCreateView.as_view(), name="message-list-create"),
    path("search/", GlobalSearchView.as_view(), name="global-search"),

]
