from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = "user_management"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("signup/", UserCreateView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-setup/", ProfileSetupView.as_view(), name="profile_setup"),
    path("liked-outfits/", LikedOutfitsView.as_view(), name="liked_outfits"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path(
        "outfit-grid-images/",
        OutfitGridImagesView.as_view(),
        name="get_outfit_images",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
