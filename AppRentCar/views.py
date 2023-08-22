from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView, \
    DeleteView

from .forms import CarForm
from .models import Car


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


