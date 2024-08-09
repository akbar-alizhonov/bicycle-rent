from django.db import models
from django.conf import settings


class Bicycle(models.Model):

    class BicycleStatus(models.TextChoices):
        available = 'available', 'AVAILABLE'
        rented = 'rented', 'RENTED'

    name = models.CharField('название велосипеда', max_length=150)
    status = models.CharField(
        max_length=10,
        choices=BicycleStatus,
        default=BicycleStatus.available,
    )
    price = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2
    )

    def __str__(self) -> str:
        return self.name


class Rental(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField('начало аренды', auto_now_add=True)
    end_time = models.DateTimeField('конец аренды', null=True, blank=True)
    cost = models.DecimalField(
        'цена',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f'Велосипед {self.bicycle.name} арендован {self.user.username}'
