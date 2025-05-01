from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    UserLoginView, UserCreateView, ProfileView, ProfileSetupView, LikedOutfitsView,
    WishlistView, OtherUserProfileView, UserFollowView
)

app_name = "user_management"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-setup/", ProfileSetupView.as_view(), name="profile_setup"),
    path("liked-outfits/", LikedOutfitsView.as_view(), name="liked_outfits"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("profile/<str:username>/", OtherUserProfileView.as_view(), name="other_user_profile"),
    path('api/followers/<str:username>/', UserFollowView().get_followers, name='get_followers'),
    path('api/following/<str:username>/', UserFollowView().get_following, name='get_following'),
    path('api/follow/<str:username>/', UserFollowView().toggle_follow, name='toggle_follow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
