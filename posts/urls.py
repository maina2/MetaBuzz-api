from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, PostSearchView, BulkPostCreateView

urlpatterns = [
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('bulk-create/', BulkPostCreateView.as_view(), name='bulk-post-create'),  # ✅ New bulk create endpoint
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
