from django.db.models import Q
from rest_framework import generics, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
import random
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ Get the User model dynamically


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BulkPostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


    def create(self, request, *args, **kwargs):
        posts_data = request.data  # Expecting a list of post dictionaries
        user_ids = list(User.objects.filter(id__lte=50).values_list("id", flat=True))  # Get available user IDs

        if not user_ids:
            return Response({"error": "No valid users found with IDs 1-50"}, status=400)

        if not isinstance(posts_data, list):
            return Response({"error": "Expected a list of posts"}, status=400)

        created_posts = []
        for post_data in posts_data:
            random_user = User.objects.get(id=random.choice(user_ids))  # ✅ Get actual user instance

            # ✅ Remove 'user' key if it exists (it must be assigned manually)
            post_data.pop("user", None)

            serializer = self.get_serializer(data=post_data)
            if serializer.is_valid():
                serializer.save(user=random_user)  # ✅ Assign user manually
                created_posts.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        return Response({"message": "Posts created successfully", "posts": created_posts}, status=201)
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

# Global Search View for Posts
class PostSearchView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Post.objects.filter(Q(content__icontains=query) | Q(user__username__icontains=query))
