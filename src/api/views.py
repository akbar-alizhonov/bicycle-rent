from django.utils import timezone
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from bicycle.models import Bicycle, Rental
from api.serializers import BicycleSerializer, RentalSerializer
from api.tasks import calculate_rental_cost


class BicycleListAPIView(generics.ListAPIView):
    ''' Возвращает список свободных велосипедов '''
    permission_classes = [AllowAny,]
    queryset = Bicycle.objects.filter(
        status=Bicycle.BicycleStatus.available
    )
    serializer_class = BicycleSerializer


class RentalCreateAPIView(APIView):
    ''' Аренда велосипеда, если пользователь еще не арендовал велоссипед '''
    permission_classes = [AllowAny,]
    serializer_class = RentalSerializer

    def post(self, request: HttpRequest, *args, **kwargs):
        bicycle = get_object_or_404(
            Bicycle,
            id=request.data['bicycle']
        )
        serializer = self.serializer_class(data=request.data)

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
    permission_classes = [AllowAny,]
    serializer_class = RentalSerializer

    def post(self, request: HttpRequest, *args, **kwargs):
        serializer = self.serializer_class(request.data)

        if serializer.is_valid(raise_exception=True):
            rental = Rental.objects.get_rental_with_bicycle().get(
                id=serializer.data['id']
            )
            bicycle = rental.bicycle

            rental.end_time = timezone.now()
            bicycle.status = Bicycle.BicycleStatus.available
            duration = rental.end_time - rental.start_time
            rental.cost = (duration.total_seconds() / 3600) * int(bicycle.price)

            rental.save()
            # calculate_rental_cost.delay(serializer.data['id'])

            return Response(
                {
                    'message': f'Вы успешно вернули велосипед {bicycle.name}'
                }
            )


class UserRentalHistoryAPIView(generics.ListAPIView):
    ''' Возвращает список, арендованных пользователем велосипедов '''
    serializer_class = RentalSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)
