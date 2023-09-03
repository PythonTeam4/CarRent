from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Car, CompanyBranches, RentalTerms, Rent, UserProfile


class CarAdmin(ModelAdmin):
    """personalization of the admin panel"""

    ordering = ["id"]
    list_display = [
        "id",
        "avatar",
        "brand",
        "model",
        "cars_type",
        "engine",
        "capacity",
        "year",
        "number_of_seats",
        "consumption",
        "power",
        "car_mileage",
        "transmission",
        "no_gears",
        "drive",
    ]


class RentalTermsAdmin(ModelAdmin):
    """personalization of the admin panel"""

    ordering = ["id"]
    list_display = ["id", "car", "price"]


class UserProfileAdmin(ModelAdmin):
    """personalization of the admin panel"""

    ordering = ["id"]
    list_display = ["id", "username", "first_name", "last_name", "email"]


class RentAdmin(ModelAdmin):
    """personalization of the admin panel"""

    ordering = ["id"]
    list_display = [
        "id",
        "client",
        "rental_terms",
        "start_date",
        "end_date",
        "take_from",
        "take_back",
        "amount",
    ]


""" Registration of models in the panel """
admin.site.register(Car, CarAdmin)
admin.site.register(CompanyBranches)
admin.site.register(RentalTerms, RentalTermsAdmin)
admin.site.register(Rent, RentAdmin)
admin.site.register(UserProfile)
