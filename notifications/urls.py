from django.urls import path
from .views import NotificationListView, mark_notifications_read

urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notification-list"),
    path("notifications/mark-read/", mark_notifications_read, name="mark-notifications-read"),
]
