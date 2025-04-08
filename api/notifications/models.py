from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("like", "Like"),
        ("comment", "Comment"),
        ("follow", "Follow"),
        ("mention", "Mention"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default="mention")
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="related_notifications")
    related_post_id = models.IntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}"
