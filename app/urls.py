from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.reference_list, name='reference_list'),
    path('reference/<int:pk>/', views.reference_detail, name='reference_detail'),
    path('reference/new/', views.reference_new, name='reference_new'),
    path('reference/<int:pk>/edit', views.reference_edit, name='reference_edit'),
    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
]