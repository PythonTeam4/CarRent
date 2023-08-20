from django.contrib import admin
from .models import Car, CompanyBranches, RentalTerms, Rent, UserProfile

admin.site.register(Car)
admin.site.register(CompanyBranches)
admin.site.register(RentalTerms)
admin.site.register(Rent)
admin.site.register(UserProfile)

