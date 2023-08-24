from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView, \
    DeleteView

from .forms import CarForm, RentForm
from .models import Car, Rent


# Create your views here.

class CarListView(ListView):
    template_name = "cars_list.html"
    model = Car


class CarDetailView(DetailView):
    template_name = "car.html"
    model = Car


class CarCreateView(FormView):
    template_name = 'form.html'
    form_class = CarForm
    success_url = '/cars/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CarUpdateView(UpdateView):
    template_name = 'form.html'
    model = Car
    fields = '__all__'

    def get_success_url(self):
        car_id = self.kwargs['pk']
        return reverse_lazy('car_detail', args=[str(car_id)])


class CarDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Car
    success_url = '/cars/'


class RentalsListView(ListView):
    template_name = "rentals_list.html"
    model = Rent


class RentalDetailView(DetailView):
    template_name = "rental.html"
    model = Rent


class RentalCreateView(FormView):
    template_name = 'form.html'
    form_class = RentForm
    success_url = '/rent/rentals/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class RentalUpdateView(UpdateView):
    template_name = 'form.html'
    model = Rent
    fields = ['rental_terms', 'client', 'start_date', 'end_date', 'take_from',
              'take_back', 'amount']

    def get_success_url(self):
        rent_id = self.kwargs['pk']
        return reverse_lazy('rental_detail', args=[str(rent_id)])


class RentalDeleteView(DeleteView):
    template_name = 'confirm_delete_reservation.html'
    model = Rent
    success_url = '/rent/rentals/'