from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import uuid

# Create your models here.


class Car(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    capacity = models.FloatField(default=65)
    gas = models.FloatField(default=0)
    num_tyres = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(4)])
    current_gas = models.FloatField(default=0)

    def __str__(self):
        return f'Car {self.id} - capacity: {self.capacity} - gas: {self.gas}% - number of tyres: {self.num_tyres}'


class Tyre(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    degradation = models.FloatField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'Tyre {self.id} - degradation: {self.degradation}%'
