from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Like, Follow
from posts.models import Post
from django.contrib.auth import get_user_model
from .serializers import LikeSerializer, FollowSerializer

User = get_user_model()
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        following = get_object_or_404(User, id=user_id)  # Fixed lookup
        if request.user == following:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if not created:
            follow.delete()
            return Response({"message": "Unfollowed user"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "User followed"}, status=status.HTTP_201_CREATED)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)  # Fixed lookup
        followers = Follow.objects.filter(following=user)
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)