from django import forms
from django.forms import Form, ValidationError, ModelChoiceField, DateTimeField, DateField
from .models import Car, Rent, RentalTerms, User, CompanyBranches


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class RentForm(forms.ModelForm):
    class Meta:
        model = Rent
        exclude = ('amount',)


