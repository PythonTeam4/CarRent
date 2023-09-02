from datetime import datetime, date

from django import forms
import django_filters
from django.db.models import Q

from .types import type_engines, type_drives, type_car, type_transmission
from .models import Car, Rent


class CarFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='rent_start_date',
        method='filter_date_range',
        label='Data od',
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today()
    )

    end_date = django_filters.DateFilter(
        field_name='rent_end_date',
        method='filter_date_range',
        label='Data do',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    engine = django_filters.MultipleChoiceFilter(
        field_name='engine',
        label='Typ silnika',
        choices=type_engines,
        widget=forms.CheckboxSelectMultiple,
    )

    transmission = django_filters.MultipleChoiceFilter(
        field_name='transmission',
        label='Skrzynia biegów',
        choices=type_transmission,
        widget=forms.CheckboxSelectMultiple,
    )

    drive = django_filters.MultipleChoiceFilter(
        field_name='drive',
        label='Napęd',
        choices=type_drives,
        widget=forms.CheckboxSelectMultiple,
    )

    cars_type = django_filters.MultipleChoiceFilter(
        field_name='cars_type',
        label='Typ samochodu',
        choices=type_car,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Car
        fields = ['engine', 'transmission', 'drive', 'cars_type']

    def filter_date_range(self, queryset, name, value):
        if not value:
            return queryset

        start_date = self.data.get('start_date')
        end_date = self.data.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
            end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
            conflicting_rents = Rent.objects.filter(
                Q(start_date__range=(start_date, end_date)) |
                Q(end_date__range=(start_date, end_date)) |
                Q(start_date__lte=start_date, end_date__gte=end_date)
            )
            reserved_cars = conflicting_rents.values_list('rental_terms__car',
                                                          flat=True)
            return queryset.exclude(id__in=reserved_cars)

        return queryset
