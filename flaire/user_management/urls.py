from django.urls import path
from .views import UserLoginView, UserCreateView, PlaceholderView

from django.conf import settings
from django.conf.urls.static import static

app_name = 'user_management'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('placeholder/', PlaceholderView.as_view(), name='placeholder'),
]