from django.urls import path
from .views import LikePostView, FollowUserView,FollowingListView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('users/following/', FollowingListView.as_view(), name='following-list'),

]
