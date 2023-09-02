from django import forms

from .models import Car, Rent, UserProfile


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control is_valid'}),
            'brand': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'model': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'cars_type': forms.Select(attrs={'class': 'form-control is_valid'}),
            'engine': forms.Select(attrs={'class': 'form-control is_valid'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control is_valid'}),
            'year': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'number_of_seats': forms.NumberInput(attrs={'class': 'form-control is_valid'}),
            'consumption': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'power': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'car_mileage': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'transmission': forms.Select(attrs={'class': 'form-control is_valid'}),
            'no_gears': forms.Select(attrs={'class': 'form-control is_valid'}),
            'drive': forms.Select(attrs={'class': 'form-control is_valid'}),
        }


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['rental_terms', 'start_date', 'end_date', 'take_from', 'take_back']
        widgets = {
            'rental_terms': forms.Select(attrs={'class': 'form-control is_valid'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control is_valid'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control is_valid'}),
            'take_from': forms.Select(attrs={'class': 'form-control is_valid'}),
            'take_back': forms.Select(attrs={'class': 'form-control is_valid'}),
        }


class AvailabilityForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
    widgets = {
        'start_date': forms.DateInput(attrs={'class': 'form-control is_valid', 'style': 'max-width: 150px;'}),
        'start_end': forms.DateInput(attrs={'class': 'form-control is_valid', 'style': 'max-width: 150px;'}),
    }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'first_name', 'last_name']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control is_valid'}),
            'phone': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control is_valid'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control is_valid'}),
        }
        labels = {
            'avatar': 'Zdjęcie',
            'phone': 'Telefon',
            'first_name': 'Imię',
            'last_name': 'Nazwisko'
        }


class DeleteCarForm(forms.Form):
    car_id = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        label='Wybierz pojazd do usunięcia',
        widget=forms.Select(attrs={'class': 'form-control is_valid'})
    )


class EditCarForm(forms.Form):
    car_id = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        label='Wybierz pojazd do edycji',
        widget=forms.Select(attrs={'class': 'form-control is_valid'})
    )
