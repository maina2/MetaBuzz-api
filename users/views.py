from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from posts.models import  Post
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, UserSerializer,PostSerializer,UserProfileWithPostsSerializer
from django.db import DatabaseError
from django.db import transaction



# Corrected: Call get_user_model() to get the User model
User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response = {
                    "message": "User registered successfully",
                    "data": serializer.data,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            except DatabaseError as e:
                return Response({"error": "Database error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)  # Serialize the user data
            response = {
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": user_serializer.data  # Use the serialized user data
            }
            return Response(data=response, status=status.HTTP_200_OK)

        return Response(data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except DatabaseError:
                return Response({"error": "Database error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received logout request with data:", request.data)  # Debugging

        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklists the token (if enabled)
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class BulkRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        users_data = request.data  # Expecting a list of users
        if not isinstance(users_data, list):
            return Response({"error": "Invalid data format. Expected a list of users."}, status=status.HTTP_400_BAD_REQUEST)

        created_users = []
        errors = []
        
        with transaction.atomic():  # Ensures rollback in case of an error
            for user_data in users_data:
                serializer = RegisterSerializer(data=user_data)
                if serializer.is_valid():
                    user = serializer.save()
                    created_users.append(serializer.data)
                else:
                    errors.append(serializer.errors)

        if errors:
            return Response({"message": "Some users could not be created", "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"{len(created_users)} users created successfully", "users": created_users}, status=status.HTTP_201_CREATED)


class UserProfileWithPostsView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(user=user).order_by('-created_at')

        serializer = UserProfileWithPostsSerializer({
            'user': user,
            'posts': posts
        })

        return Response(serializer.data, status=status.HTTP_200_OK)