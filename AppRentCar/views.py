from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView, \
    DeleteView, CreateView, TemplateView

from .forms import CarForm, RentForm, AvailabilityForm, UserProfileForm
from .models import Car, Rent, RentalTerms, UserProfile
from datetime import datetime


class HomeView(TemplateView):
    template_name = 'home.html'


class CarListView(ListView):
    template_name = "cars_list.html"
    model = Car


class CarDetailView(DetailView):
    template_name = "car.html"
    model = Car


class CarCreateView(FormView):
    template_name = 'form.html'
    form_class = CarForm
    success_url = reverse_lazy('cars')

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
    success_url = reverse_lazy('cars')


class RentCreateView(LoginRequiredMixin, CreateView):
    model = Rent
    form_class = RentForm
    template_name = 'create_rent.html'
    success_url = reverse_lazy('cars')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.kwargs.get('car_id')
        car = get_object_or_404(Car, pk=car_id)
        context['car'] = car

        form = self.get_form()
        form.fields['rental_terms'].queryset = RentalTerms.objects.filter(car_id=car_id)
        context['form'] = form

        return context

    def form_valid(self, form):
        car_id = self.kwargs.get('car_id')
        car = get_object_or_404(Car, pk=car_id)
        rental_terms = form.cleaned_data['rental_terms']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        period = (end_date - start_date).days
        rental_price = rental_terms.price
        rent = form.save(commit=False)
        rent.car = car
        rent.amount = rental_price * period
        rent.client = self.request.user
        return super().form_valid(form)


class SubmittableLoginView(LoginView):
    template_name = 'form.html'
    next_page = reverse_lazy('cars')


class RegisterView(CreateView):
    template_name = 'form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class Logout(LogoutView):
    next_page = reverse_lazy('cars')


class UserRentalsView(LoginRequiredMixin, ListView):
    template_name = 'user_rentals.html'
    model = Rent
    context_object_name = 'rentals'

    def get_queryset(self):
        user = self.request.user
        return Rent.objects.filter(client=user)


class AvailableCarsView(ListView):
    model = Car
    template_name = 'available_cars.html'
    context_object_name = 'available_cars'
    form_class = AvailabilityForm  # Twój formularz do wybierania daty

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            conflicting_rents = Rent.objects.filter(
                Q(start_date__range=(start_date, end_date)) |
                Q(end_date__range=(start_date, end_date)) |
                Q(start_date__lte=start_date, end_date__gte=end_date)
            )
            reserved_cars = conflicting_rents.values_list('rental_terms__car', flat=True)
            available_cars = Car.objects.exclude(id__in=reserved_cars)
        else:
            available_cars = Car.objects.all()

        return available_cars

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(self.request.GET)
        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profil.html'
    context_object_name = 'user_profile'
    login_url = '/login/'

    def get_object(self, queryset=None):
        return self.request.user.userprofile


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'edit_profile.html'
    success_url = '/profil/'

    def get_object(self, queryset=None):
        return self.request.user.userprofile