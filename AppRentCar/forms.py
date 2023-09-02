from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Car, Rent, RentalTerms, UserProfile


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ['rental_terms', 'start_date', 'end_date', 'take_from', 'take_back']
        widgets = {
            'rental_terms': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'take_from': forms.Select(attrs={'class': 'form-select'}),
            'take_back': forms.Select(attrs={'class': 'form-select'}),
        }


class SignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    phone = forms.CharField(max_length=32)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'phone', 'password1', 'password2', 'avatar']

    def save(self, commit=True):
        self.instance.is_active = False
        return super().save(commit)


class AvailabilityForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone']


class DeleteCarForm(forms.Form):
    car_id = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        label='Wybierz pojazd do usunięcia',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class EditCarForm(forms.Form):
    car_id = forms.ModelChoiceField(
        queryset=Car.objects.all(),
        label='Select Car to Edit',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
