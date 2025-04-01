from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.serializers import PostSerializer
from posts.serializers import CommentSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    
    def get_followers_count(self, obj):
        return obj.followers.count()  

    def get_following_count(self, obj):
        return obj.following.count() 
        
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 
                 'profile_picture', 'phone', 'followers_count', 'following_count']
        read_only_fields = ['id', 'username', 'email', 'followers_count', 'following_count']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.profile_picture:
            rep['profile_picture'] = instance.profile_picture.url
        else:
            rep['profile_picture'] = None
        return rep

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    bio = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)  # Assuming this is an ImageField
    phone = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'bio', 'profile_picture', 'phone')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  
        user.save()
        return user
    

# serializers.py

class UserProfileWithPostsSerializer(serializers.Serializer):
    user = UserSerializer()
    posts = PostSerializer(many=True)
