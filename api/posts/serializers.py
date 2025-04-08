from rest_framework import serializers
from .models import Post, Comment



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  
    user = serializers.PrimaryKeyRelatedField(read_only=True)  

    def to_representation(self, instance):
        from users.serializers import UserSerializer  
        rep = super().to_representation(instance)
        rep['user'] = UserSerializer(instance.user).data
        return rep

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_at','comments']
        extra_kwargs = {
            'content': {'required': False}, 
            'image': {'required': False},   
        }
