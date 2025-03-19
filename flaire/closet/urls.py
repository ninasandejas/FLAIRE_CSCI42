from django.urls import path

from .views import *

urlpatterns = [
    path("", closet, name="closet"),
]

app_name = "closet"
