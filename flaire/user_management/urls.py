from django.urls import path
from .views import UserUpdateView, UserCreateView


app_name = 'user_management'

urlpatterns = [
    path('profile/', UserUpdateView.as_view(), name='user_detail'),
    path('registration/', UserCreateView.as_view(), name='user_registration'),
]