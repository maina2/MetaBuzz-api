from django.urls import path
from .views import CreateCommentView,PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, PostSearchView, BulkPostCreateView,PostCommentsListView

urlpatterns = [
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('bulk-create/', BulkPostCreateView.as_view(), name='bulk-post-create'),  # ✅ New bulk create endpoint
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:post_id>/comments/', PostCommentsListView.as_view(), name='post-comments'),
    path("<int:post_id>/comments/create/", CreateCommentView.as_view(), name="create-comment"),


]
