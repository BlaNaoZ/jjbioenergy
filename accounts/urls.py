from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.profile, name='profile'),
    path('list', views.profile_list, name='profile_list'),
    path('<int:pk>/favourites', views.favourite_list, name='favourite_list'),
]