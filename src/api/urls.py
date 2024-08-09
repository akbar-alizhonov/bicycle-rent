from django.urls import path

from api import views


urlpatterns = [
    path('', views.BicycleListAPIView.as_view(), name='bicycle_list'),
    path(
        'create-rental/',
        views.RentalCreateAPIView.as_view(),
        name='create_rental'
    ),
    path(
        'return/',
        views.ReturnBicycleAPIView.as_view(),
        name='return_bicycle'
    ),
    path('history/', views.UserRentalHistoryAPIView.as_view(), name='history')
]
