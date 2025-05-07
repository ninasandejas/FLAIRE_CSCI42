from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

app_name = "social"

urlpatterns = [

    path("explore-outfits/", ExploreOutfitsGridView.as_view(), name="explore-outfits"),
    path("explore-showrooms/", ExploreShowroomsGridView.as_view(), name="explore-showrooms"),
    path("following-outfits/", FollowingOutfitsGridView.as_view(), name="following-outfits"),
    path("following-showrooms/", FollowingShowroomsGridView.as_view(), name="following-showrooms"),
    path("outfit-details/<int:pk>/", OutfitDetailView.as_view(), name="outfit_details"),
    path(
        "submit-comment/<int:outfit_id>/",
        SubmitCommentView.as_view(),
        name="submit-comment",
    ),
]



