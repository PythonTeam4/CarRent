from django.urls import path

from .views import (CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView, RentCreateView,
                    SubmittableLoginView, RegisterView, Logout, UserRentalsView, HomeView, AvailableCarsView,
                    UserProfileView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cars/', CarListView.as_view(), name="cars"),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', CarCreateView.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='cars_delete'),
    path('create_rent/<int:car_id>/', RentCreateView.as_view(), name='create_rent'),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('sign_up/', RegisterView.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('my-rentals/', UserRentalsView.as_view(), name='user_rentals'),
    path('available-cars/', AvailableCarsView.as_view(), name='available_cars'),
    path('profil/', UserProfileView.as_view(), name='user_profile'),
]
