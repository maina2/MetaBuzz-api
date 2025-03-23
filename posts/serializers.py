from rest_framework import serializers
from .models import Post, Comment
from users.serializers import UserSerializer  # assuming you have one


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) 
    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at']
