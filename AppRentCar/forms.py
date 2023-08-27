from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Car, Rent, RentalTerms


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['rental_terms', 'start_date', 'end_date', 'take_from', 'take_back']

    def __init__(self, *args, **kwargs):
        car_id = kwargs.pop('car_id', None)
        user_is_premium = kwargs.pop('user_is_premium', False)
        super().__init__(*args, **kwargs)
        self.user_is_premium = user_is_premium

        if car_id:
            rental_terms_queryset = RentalTerms.objects.filter(car_id=car_id)
            if user_is_premium:
                rental_terms_queryset = rental_terms_queryset.filter(premium_price__isnull=False)
            else:
                rental_terms_queryset = rental_terms_queryset.filter(premium_price__isnull=True)
            self.fields['rental_terms'].queryset = rental_terms_queryset

    def get_rental_terms_choices(self):
        choices = []
        for rental_terms in self.fields['rental_terms'].queryset:
            if self.user_is_premium:
                price_display = f"Premium: {rental_terms.premium_price}"
            else:
                price_display = f"Regular: {rental_terms.regular_price}"
            choices.append((rental_terms.id, f"{rental_terms.car.brand} {rental_terms.car.model} - {price_display}"))
        return choices


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name']

    def save(self, commit=True):
        self.instance.is_active = False
        return super().save(commit)


class AvailabilityForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
