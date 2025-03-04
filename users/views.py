from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, UserSerializer

User= get_user_model

class RegisterView(APIView):
    permission_classes=AllowAny
    

    def post(self,reqest,*args, **kwargs):
        serializer=RegisterSerializer(data=reqest.data);
        if serializer.is_valid():
            user=serializer.save()
            refresh= RefreshToken.for_user(user)
            response = {
                "message": "User registered successfully",
                "data": serializer.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes=AllowAny

    def post(request,*args, **kwargs):
        username=request.data.get("username")
        password=request.data.ger("password")

        user=authenticate(username=username,password=password)
        if user:
            refresh=RefreshToken.for_user(user)
            response={
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "username": user.username,
                    "email": user.email,
                }
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
            if 'profile_picture' in request.data:  # Handle image upload separately
                user.profile_picture = request.data['profile_picture']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
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