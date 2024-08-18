from django.db import models


class RentalManager(models.Manager):
    def get_rental_with_bicycle(self):
        rental = self.get_queryset().select_related('bicycle')
        return rental
