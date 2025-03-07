from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url  # Cloudinary provides the full URL
        return None

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        read_only_fields = ('id',)  # Ensure this is a tuple
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'bio', 'profile_picture', 'phone')

    def create(self, validated_data):
        # Extract the password from validated_data
        password = validated_data.pop('password')
        # Create the user using create_user (handles password hashing)
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Set the password (optional, as create_user already handles it)
        user.save()
        return user