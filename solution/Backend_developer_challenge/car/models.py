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
        self.num_tyres = Tyre.objects.filter(car_id=self.id).count()
        return f'Car {self.id} - capacity: {self.capacity} - gas: {self.gas}% - number of tyres: {self.num_tyres}'

    @property
    def getCurrentGas(self):
        self.current_gas = 100 * (self.gas / self.capacity)
        self.save()

    @property
    def countTyres(self):
        self.num_tyres = Tyre.objects.filter(car_id=self.id).count()
        return f'{self.num_tyres} tyres'

    def trip(self, distance):
        self.num_tyres = Tyre.objects.filter(car_id=self.id).count()
        if (self.num_tyres == 4):
            if (self.gas - distance / 8 < 0):
                self.gas = 0
            else:
                self.gas -= distance / 8
            self.save()

    def refuel(self, gas):
        if (self.gas + gas > self.capacity):
            self.gas = self.capacity
        else:
            self.gas += gas
        self.save()

    def maintenance(self, tyre):
        pass


class Tyre(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    degration = models.FloatField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if Tyre.objects.filter(car=self.car).count() == 4:
            raise ValidationError('The car already has 4 tyres')
        return super(Tyre, self).save(*args, **kwargs)

    def __str__(self):
        return f'Tyre {self.id} - degradation: {self.degration}%'

    def trip(self, distance):
        if (self.degration + distance / 3 < 94):
            self.degration += distance / 3
        if (self.degration > 94):
            self.delete()
        else:
            self.save()
