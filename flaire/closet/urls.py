from django.urls import path

from . import views
from .views import *

app_name = "closet"

urlpatterns = [
    path("images/", views.clothing_item_images, name="get_clothing_images"),
    path("", closet, name="closet"),
    path("add/", views.add_clothing_item, name="add_clothing_item"),
]
