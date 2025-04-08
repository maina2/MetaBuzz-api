from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Like, Follow
from posts.models import Post
from django.contrib.auth import get_user_model
from .serializers import LikeSerializer, FollowSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_204_NO_CONTENT)

        #    Send real-time notification
        send_notification(post.user.id, f"{request.user.username} liked your post.")

        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ToggleFollowView(APIView):
    """
    View to handle following and unfollowing users
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to follow/unfollow
        target_user = get_object_or_404(User, id=user_id)
        
        # Prevent self-following
        if request.user.id == user_id:
            return Response(
                {"error": "You cannot follow/unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        existing_follow = Follow.objects.filter(
            follower=request.user, 
            followed=target_user
        ).first()
        
        if existing_follow:
            # Unfollow
            existing_follow.delete()
            message = "User unfollowed"
            is_following = False
        else:
            # Follow
            Follow.objects.create(
                follower=request.user, 
                followed=target_user
            )
            message = "User followed"
            is_following = True
        
        # Get updated followers count for the target user
        followers_count = target_user.followers.count()
        
        return Response({
            "message": message,
            "is_following": is_following,
            "followers_count": followers_count
        }, status=status.HTTP_200_OK)


class FollowedUsersListView(APIView):
    """
    View to retrieve list of followed users
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all users the current user is following
        followed_users = Follow.objects.filter(follower=request.user)
        
        # Serialize the followed users
        serializer = FollowSerializer(followed_users, many=True)
        
        # Return only the followed user IDs and usernames
        return Response(
            [
                {
                    "id": follow.followed.id, 
                    "username": follow.followed.username
                } 
                for follow in followed_users
            ],
            status=status.HTTP_200_OK
        )
#    Notification function
def send_notification(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user_id}",
        {"type": "send_notification", "data": {"message": message}}
    )

