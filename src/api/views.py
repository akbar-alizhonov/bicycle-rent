from django.utils import timezone
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from bicycle.models import Bicycle, Rental
from api.serializers import BicycleSerializer, RentalSerializer
from api.tasks import calculate_rental_cost


class BicycleListAPIView(generics.ListAPIView):
    ''' Возвращает список свободных велосипедов '''
    permission_classes = [IsAuthenticated,]
    queryset = Bicycle.objects.filter(
        status=Bicycle.BicycleStatus.available
    )
    serializer_class = BicycleSerializer


class RentalCreateAPIView(APIView):
    ''' Аренда велосипеда, если пользователь еще не арендовал велоссипед '''
    permission_classes = [IsAuthenticated,]

    def post(self, request: HttpRequest, *args, **kwargs):
        bicycle = get_object_or_404(
            Bicycle,
            id=request.data['bicycle']
        )
        serializer = RentalSerializer(data=request.data)

        if (
            Rental.objects.filter(
                user=self.request.user,
                end_time__isnull=True
            ).exists()
        ):
            return Response(
                {
                    'message': (
                        'Вы уже арендовали велосипед'
                        ', верните велосипед, чтобы арендовать новый'
                    )
                }
            )

        if (
            serializer.is_valid(raise_exception=True)
            and bicycle.status == Bicycle.BicycleStatus.available
        ):
            serializer.save()
            bicycle.status = Bicycle.BicycleStatus.rented
            bicycle.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ReturnBicycleAPIView(APIView):
    ''' Возврат велосипеда '''
    permission_classes = [IsAuthenticated,]

    def post(self, request: HttpRequest, *args, **kwargs):
        rental = get_object_or_404(
            Rental,
            id=request.data['bicycle']
        )
        rental.end_time = timezone.now()
        calculate_rental_cost.delay(request.data['bicycle'])

        rental.save()
        return Response(
            {
                'message': f'Вы успешно вернули велосипед {rental.bicycle.name}'
            }
        )


class UserRentalHistoryAPIView(generics.ListAPIView):
    ''' Возвращает список, арендованных пользователем велосипедов '''
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)
