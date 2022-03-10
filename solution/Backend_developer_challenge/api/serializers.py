from rest_framework import serializers
from car.models import Car, Tyre


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class TyreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tyre
        fields = '__all__'
