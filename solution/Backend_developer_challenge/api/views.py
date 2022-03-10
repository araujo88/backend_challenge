from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CarSerializer, TyreSerializer
from car.models import Car, Tyre

# Create your views here.


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'POST': '/api/trip'},
        {'POST': '/api/refuel'},
        {'POST': '/api/maintenance'},
        {'POST': '/api/create-car'},
        {'POST': '/api/create-tyre'},
        {'GET': '/api/get-car-status/id'},
        {'GET': '/api/get-cars'},
        {'GET': '/api/get-tyres'},
    ]

    return Response(routes)


@api_view(['GET'])
def getCars(request):
    pass


@api_view(['GET'])
def getTyres(request):
    pass


@api_view(['GET'])
def getCarStatus(request, pk):
    car = Car.objects.get(id=pk)
    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def trip(request, pk):
    pass


@api_view(['POST'])
def refuel(request, pk):
    pass


@api_view(['POST'])
def maintenance(request, pk):
    pass


@api_view(['POST'])
def createCar(request):
    pass


@api_view(['POST'])
def createTyre(request, pk):
    pass
