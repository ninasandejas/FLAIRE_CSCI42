from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import toggle_wishlist
from . import views
from .views import unlike_outfit



from .views import (
    LikedOutfitsView,
    OtherUserProfileView,
    OutfitDetailView,
    OutfitGridImagesView,
    ProfileSetupView,
    ProfileView,
    SubmitCommentView,
    UserCreateView,
    UserFollowView,
    UserLoginView,
    WishlistView,
)

app_name = "user_management"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-setup/", ProfileSetupView.as_view(), name="profile_setup"),
    path("liked-outfits/", LikedOutfitsView.as_view(), name="liked_outfits"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path(
        "profile/<str:username>/",
        OtherUserProfileView.as_view(),
        name="other_user_profile",
    ),
    path(
        "api/followers/<str:username>/",
        UserFollowView().get_followers,
        name="get_followers",
    ),
    path(
        "api/following/<str:username>/",
        UserFollowView().get_following,
        name="get_following",
    ),
    path(
        "api/follow/<str:username>/",
        UserFollowView().toggle_follow,
        name="toggle_follow",
    ),
    path(
        "outfit-grid-images/",
        OutfitGridImagesView.as_view(),
        name="get_outfit_images",
    ),
    path(
        "outfit-grid-images/<str:username>/",
        OutfitGridImagesView.as_view(),
        name="get_outfit_images",
    ),
    path("outfit-details/<int:pk>/", OutfitDetailView.as_view(), name="outfit_details"),
    path(
        "submit-comment/<int:outfit_id>/",
        SubmitCommentView.as_view(),
        name="submit-comment",
    ),
    path("toggle-wishlist/<int:item_id>/", toggle_wishlist, name="toggle_wishlist"),
    path("toggle-like-outfit/<int:outfit_id>/", toggle_like_outfit, name="toggle_like_outfit"),
    path("remove-from-wishlist/<int:item_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
     path("unlike-outfit/<int:outfit_id>/", views.unlike_outfit, name="unlike_outfit"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
