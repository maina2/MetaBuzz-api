from django.urls import path
from .views import LikePostView, ToggleFollowView,FollowedUsersListView

urlpatterns = [
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    # path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    # path('users/following/', FollowingListView.as_view(), name='following-list'),

    path('<int:user_id>/follow/', ToggleFollowView.as_view(), name='toggle-follow'),
    path('users/following/', FollowedUsersListView.as_view(), name='followed-users'),



]
