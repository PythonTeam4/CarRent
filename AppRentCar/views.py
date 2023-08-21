from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Car


# Create your views here.

class CarListView(ListView):
    template_name = "cars_list.html"
    model = Car


class CarDetailView(DetailView):
    template_name = "car.html"
    model = Car

