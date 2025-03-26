from django.db import models
from django.conf import settings
from posts.models import Post
from django.contrib.auth import get_user_model


User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensures a user can like a post only once

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"



class Follow(models.Model):

    follower = models.ForeignKey(
        User, 
        related_name='following', 
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, 
        related_name='followers', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"