from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('get-car-status/<str:pk>/', views.getCarStatus),
]
