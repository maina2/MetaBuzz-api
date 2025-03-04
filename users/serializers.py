from django.contrib.auth import get_user_model
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    profile_picture=serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url  # Cloudinary provides the full URL
        return None

    class Meta:
        model=get_user_model
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture')
        read_only_fields=('id')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model=get_user_model
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'bio', 'profile_picture','phone')

    def create(self, validated_data):
        password= validated_data.pop('password')
        user= get_user_model.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user