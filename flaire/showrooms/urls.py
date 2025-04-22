from django.urls import path

from flaire import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from .views import *

app_name = "showrooms"

urlpatterns = [
    path("", views.showrooms, name="showrooms"),
    path("owned/", views.list_of_showrooms, name="get_showrooms_owned"),
    path("create/", views.create_showroom, name="create_showrooms"),
    path('<int:pk>/', views.showroom_detail, name='showroom_detail'),
    path('<int:pk>/outfits/', views.showroom_outfits, name='showroom_outfits'),
    path('<int:pk>/update/', views.edit_showroom, name='edit_showroom'),
    path('<int:pk>/follow/', views.follow_showroom, name='follow_showroom'),
] 
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += staticfiles_urlpatterns()