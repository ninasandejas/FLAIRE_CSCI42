from django.urls import path

from . import views
from .views import *

app_name = "showrooms"

urlpatterns = [
    path("", views.showrooms, name="showrooms"),
    path("owned/", views.list_of_showrooms, name="get_showrooms_owned"),
    # path("add-showrooms/", views.add_showrooms, name="add_showrooms"),
]
