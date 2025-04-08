from django.urls import path
from .views import RegisterView, UserProfileWithPostsView,LoginView, UserProfileView, LogoutView, BulkRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register-user"),
    path("login/", LoginView.as_view(), name="login-user"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('profile/<int:user_id>/', UserProfileWithPostsView.as_view(), name='user-profile-with-posts'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("bulk/register/", BulkRegisterView.as_view(), name="bulk-register"),  
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
]
