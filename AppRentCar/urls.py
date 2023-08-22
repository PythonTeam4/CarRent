from django.urls import path

from .views import CarListView, CarDetailView, CarCreateView, CarUpdateView, \
    CarDeleteView

urlpatterns = [
    path('cars/', CarListView.as_view(), name="cars"),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', CarCreateView.as_view(), name='cars_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='cars_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='cars_delete')
]
