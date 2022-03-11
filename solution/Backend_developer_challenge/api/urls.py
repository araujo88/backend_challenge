from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('trip/<str:pk>', views.trip),
    path('refuel/<str:pk>', views.refuel),
    path('maintenance/<str:pk>', views.maintenance),
    path('create-car/', views.createCar),
    path('create-tyre/', views.createTyre),
    path('get-car-status/<str:pk>', views.getCarStatus),
    path('get-cars/', views.getCars),
    path('get-tyres/', views.getTyres),
]
