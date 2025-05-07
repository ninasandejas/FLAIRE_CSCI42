from django.urls import path

from . import views
from .views import *

app_name = "closet"

urlpatterns = [
    path("images/", views.clothing_item_images, name="get_clothing_images"),
    path("", closet, name="closet"),
    path("add-clothing-item/", views.add_clothing_item, name="add_clothing_item"),
    path("save-outfit/", views.save_outfit, name="save_outfit"),
    path(
        "save-outfit-post-metadata/<int:outfit_id>/",
        views.save_outfit_post_metadata,
        name="save_outfit_post_metadata",
    ),
    path("select-ootd/<int:outfit_id>/", views.select_ootd, name="select_ootd"),
    path("delete-ootd/", views.delete_ootd, name="delete_ootd"),
]
