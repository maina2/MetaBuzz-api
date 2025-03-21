from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        return obj.profile_picture.url if obj.profile_picture else None

    def get_followers_count(self, obj):
        return obj.followers.count()  

    def get_following_count(self, obj):
        return obj.following.count() 

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 
            'profile_picture', 'followers_count', 'following_count'
        )
        read_only_fields = ('id',)

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