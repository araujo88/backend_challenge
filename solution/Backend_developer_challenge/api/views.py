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
        {'POST': '/api/trip/id'},
        {'POST': '/api/refuel/id'},
        {'POST': '/api/maintenance/id'},
        {'POST': '/api/create-car'},
        {'POST': '/api/create-tyre'},
        {'GET': '/api/get-car-status/id'},
        {'GET': '/api/get-cars'},
        {'GET': '/api/get-tyres'},
    ]

    return Response(routes)


@api_view(['GET'])
def getCars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTyres(request):
    tyres = Tyre.objects.all()
    serializer = TyreSerializer(tyres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCarStatus(request, pk):
    car = Car.objects.get(id=pk)
    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def trip(request, pk):
    car = Car.objects.get(id=pk)
    data = request.data
    distance = float(data['distance'])
    car.num_tyres = Tyre.objects.filter(car=car).count()

    if (car.num_tyres == 4):
        if (car.gas - distance / 8. <= 0):
            car.gas = 0.
            car.current_gas = 0.
        else:
            car.gas -= distance / 8.
            car.current_gas = 100. * (car.gas / car.capacity)
        car.save()

        tyres = Tyre.objects.filter(car=car)
        for tyre in tyres:
            if (tyre.degradation == 100):
                tyre.delete()
                break
            if (tyre.degradation + distance / 3. <= 100):
                tyre.degradation += distance / 3.
                tyre.save()
            else:
                tyre.degradation = 100
            tyre.save()

    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def refuel(request, pk):
    car = Car.objects.get(id=pk)
    data = request.data
    gas = float(data['gas'])

    if (car.current_gas < 5.):
        if (car.gas + gas >= car.capacity):
            car.gas = car.capacity
        else:
            car.gas += gas
        car.current_gas = 100 * (car.gas / car.capacity)
        car.save()

    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def maintenance(request, pk):
    car = Car.objects.get(id=pk)
    tyres = Tyre.objects.filter(car=car)

    for tyre in tyres:
        if (tyre.degradation > 94.):
            tyre.delete()
            new_tyre = Tyre(car=car)
            new_tyre.save()
            car.num_tyres += 1
            car.save()

    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createCar(request):
    car = Car()
    car.save()
    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createTyre(request):
    data = request.data
    pk = data['id']
    tyre = Tyre()
    tyre.car = Car.objects.get(id=pk)
    tyre.save()
    tyre.car.num_tyres += 1
    tyre.car.save()
    serializer = TyreSerializer(tyre, many=False)
    return Response(serializer.data)
