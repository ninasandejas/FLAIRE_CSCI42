from django.urls import path

from . import views
from .views import *

app_name = "social"

urlpatterns = [
    path('explore/', views.explore, name='explore'),
    path('following/', views.following, name='following'),
    path('notifications/', views.fetch_notifications, name='notifs')
]

