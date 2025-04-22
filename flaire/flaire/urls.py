"""flaire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.contrib.auth import views as auth_views
from user_management.views import LikedOutfitsView



def home(request):
    return render(request, "home.html", {"active_tab": "home"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user_management.urls")),
    path("closet/", include("closet.urls", namespace="closet")),
    path("", home, name="home"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("showrooms/", include("showrooms.urls", namespace="showrooms")),
    path("social/", include("social.urls", namespace="social")),
    path('liked-outfits/', LikedOutfitsView.as_view(), name='liked_outfits'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
