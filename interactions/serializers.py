from rest_framework import serializers
from .models import Like, Follow
from django.contrib.auth import get_user_model
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Shows the username instead of ID
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']


User = get_user_model()

class UserFollowSerializer(serializers.ModelSerializer):
    """
    Serializer for user follow/unfollow actions
    """
    class Meta:
        model = User
        fields = ['id', 'username']

class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for Follow model
    """
    follower = UserFollowSerializer(read_only=True)
    followed = UserFollowSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'followed', 'created_at']

class UserFollowSerializer(serializers.ModelSerializer):
    """
    Serializer for user follow/unfollow actions
    """
    class Meta:
        model = User
        fields = ['id', 'username']
