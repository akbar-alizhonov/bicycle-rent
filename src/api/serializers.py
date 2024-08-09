from rest_framework import serializers

from bicycle.models import Bicycle, Rental


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = [
            'id',
            'name',
            'status',
            'price'
        ]


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            'id',
            'user',
            'bicycle',
            'cost',
        ]
