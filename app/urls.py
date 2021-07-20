from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.reference_list, name='reference_list'),
    path('reference/<int:pk>/', views.reference_detail, name='reference_detail'),
]