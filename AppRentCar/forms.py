from django import forms

from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = (
            'avatar',
            'brand',
            'model',
            'cars_type',
            'engine',
            'capacity',
            'year',
            'number_of_seats',
            'consumption',
            'power',
            'car_mileage',
            'transmission',
            'no_gears',
            'drive',
        )
