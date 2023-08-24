from django.urls import path

from .views import CarListView, CarDetailView, CarCreateView, CarUpdateView, \
    CarDeleteView, RentalsListView, RentalDetailView, RentalCreateView, RentalUpdateView, RentalDeleteView

urlpatterns = [
    path('cars/', CarListView.as_view(), name="cars"),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', CarCreateView.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='cars_delete'),
    path('rent/rentals/', RentalsListView.as_view(), name='rentals'),
    path('rent/rentals/<int:pk>/', RentalDetailView.as_view(), name='rental_detail'),
    path('rent/create/', RentalCreateView.as_view(), name='rental_create'),
    path('rent/rentals/<int:pk>/update/', RentalUpdateView.as_view(), name='rental_update'),
    path('rent/rentals/<int:pk>/delete/', RentalDeleteView.as_view(), name='rental_delete'),
]
