from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

app_name = "social"

urlpatterns = [
    path("explore/", explore, name="explore"),
    path("following/", following, name="following"),
    path("explore-outfits/", ExploreOutfitsGridView.as_view(), name="explore-outfits"),
    path(
        "explore-showrooms/",
        ExploreShowroomsGridView.as_view(),
        name="explore-showrooms",
    ),
    path(
        "following-outfits/",
        FollowingOutfitsGridView.as_view(),
        name="following-outfits",
    ),
    path(
        "following-showrooms/",
        FollowingShowroomsGridView.as_view(),
        name="following-showrooms",
    ),
    path("notifications/", fetch_notifications, name="notifs"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
