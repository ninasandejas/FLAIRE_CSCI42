from django.urls import path

from . import views
from .views import *

app_name = "social"

urlpatterns = [
    path("explore/", views.ExploreView.as_view(), name="explore"),
    path("following/", views.FollowingView.as_view(), name="following"),
]
