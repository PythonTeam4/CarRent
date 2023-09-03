from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, UpdateView, \
    DeleteView, CreateView, TemplateView
from django_filters.views import FilterView

from .forms import CarForm, RentForm, UserProfileForm, DeleteCarForm, EditCarForm
from .models import Car, Rent, RentalTerms, UserProfile
from datetime import date, timedelta
from .filters import CarFilter


class HomeView(FilterView):
    model = Car
    context_object_name = "cars_list"
    template_name = "home.html"
    filterset_class = CarFilter

    def get_filterset_kwargs(self, *args, **kwargs):
        filterset_kwargs = super().get_filterset_kwargs(*args, **kwargs)
        data = self.request.GET.copy()
        if 'start_date' not in data:
            data['start_date'] = date.today().strftime('%Y-%m-%d')
        if 'end_date' not in data:
            data['end_date'] = (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')
        filterset_kwargs['data'] = data
        return filterset_kwargs


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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Brak dostępu. Tylko personel ma uprawnienia do dodawania samochodów.")
        return super().dispatch(request, *args, **kwargs)


class CarUpdateView(UpdateView):
    template_name = 'form.html'
    model = Car
    fields = '__all__'

    def get_success_url(self):
        car_id = self.kwargs['pk']
        return reverse_lazy('car_detail', kwargs={'pk': car_id})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Brak dostępu. Tylko personel ma uprawnienia do edycji samochodów.")
        return super().dispatch(request, *args, **kwargs)


class CarDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Car
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("Brak dostępu. Tylko personel ma uprawnienia do usuwania samochodów.")
        return super().dispatch(request, *args, **kwargs)


class RentCreateView(LoginRequiredMixin, CreateView):
    model = Rent
    form_class = RentForm
    template_name = 'create_rent.html'
    success_url = reverse_lazy('home')

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
    next_page = reverse_lazy('home')


class RegisterView(CreateView):
    template_name = 'form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class Logout(LogoutView):
    next_page = reverse_lazy('home')


class UserRentalsView(LoginRequiredMixin, ListView):
    template_name = 'user_rentals.html'
    model = Rent
    context_object_name = 'rentals'

    def get_queryset(self):
        user = self.request.user
        return Rent.objects.filter(client=user)


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


class AdminOnlyView(UserPassesTestMixin, TemplateView):
    template_name = 'admin_panel.html'

    def test_func(self):
        return self.request.user.is_superuser


class DeleteCarFromList(FormView):
    template_name = 'delete_car_list.html'
    form_class = DeleteCarForm

    def form_valid(self, form):
        car_id = form.cleaned_data['car_id']
        car = get_object_or_404(Car, id=car_id)
        car.delete()
        return redirect('admin_panel')


class EditCarFromList(FormView):
    template_name = 'edit_car_list.html'
    form_class = EditCarForm

    def form_valid(self, form):
        car_id = form.cleaned_data['car_id']
        return redirect('cars_update', pk=car_id.id)


class RentAdminView(ListView):
    template_name = 'rent_admin.html'
    model = Rent

    context_object_name = 'rents'

    def get_queryset(self):
        return Rent.objects.all()
