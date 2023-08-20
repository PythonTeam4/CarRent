from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Car, CompanyBranches, RentalTerms, Rent, UserProfile


class CarAdmin(ModelAdmin):
    ordering = ['id']
    list_display = [
        'id', 'avatar', 'brand', 'model', 'cars_type', 'engine', 'capacity', 'year', 'number_of_seats', 'consumption',
        'power',
        'car_mileage', 'transmission', 'no_gears', 'drive']


class RentalTermsAdmin(ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'car', 'price']


class UserProfileAdmin(ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']


class RentAdmin(ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'client', 'rental_terms', 'start_date', 'end_date', 'take_from', 'take_back', 'amount']


admin.site.register(Car, CarAdmin)
admin.site.register(CompanyBranches)
admin.site.register(RentalTerms, RentalTermsAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(UserProfile)
