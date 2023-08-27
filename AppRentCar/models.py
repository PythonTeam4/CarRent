from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.contrib.auth.models import User

from .types import *


class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Car(BaseModel):
    """Car Model"""

    avatar = models.ImageField(
        upload_to='media/avatars/', blank=True, null=True)
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 80}
    )
    brand = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    cars_type = models.CharField(max_length=32, choices=type_car)
    engine = models.CharField(max_length=32, choices=type_engines)
    capacity = models.FloatField()
    year = models.CharField(max_length=8)
    number_of_seats = models.IntegerField()
    consumption = models.CharField(max_length=32)
    power = models.CharField(max_length=16)
    car_mileage = models.CharField(max_length=16)
    transmission = models.CharField(max_length=32, choices=type_transmission)
    no_gears = models.CharField(max_length=8, choices=number_of_gears)
    drive = models.CharField(max_length=32, choices=type_drives)

    def __str__(self):
        return f"{self.brand} {self.model} {self.year}"


class UserProfile(BaseModel):
    """User Profile class """
    avatar = models.ImageField(
        upload_to='media/avatars/', blank=True, null=True)
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 80})
    phone = models.CharField(max_length=32)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rentals_count = models.PositiveIntegerField(default=0)

    def is_premium(self):
        return self.rentals_count >= 26

    def get_display_price(self):
        if self.is_premium():
            return "Premium"
        else:
            return "Regular"

    def __str__(self):
        return f"{self.user.username} - {self.get_display_price()}"


class CompanyBranches(BaseModel):
    """Comapny Branches"""
    city = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return f"{self.city}"


class RentalTerms(BaseModel):
    """Rental Terms class """
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    regular_price = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    premium_price = models.DecimalField(max_digits=16, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.car.brand} {self.car.model}"


class Rent(BaseModel):
    """Rent class """
    rental_terms = models.ForeignKey(RentalTerms, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    take_from = models.ForeignKey(
        CompanyBranches, related_name='rents_taken', on_delete=models.CASCADE)
    take_back = models.ForeignKey(
        CompanyBranches, related_name='rents_returned', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def clean(self):
        if not self.is_car_available():
            raise (ValidationError
                   ("This car is not available for the selected date"))

    def is_car_available(self):
        if self.id is None:
            conflicting_rents = Rent.objects.filter(
                Q(rental_terms__car=self.rental_terms.car),
                Q(start_date__range=(self.start_date, self.end_date)) |
                Q(end_date__range=(self.start_date, self.end_date)) |
                Q(start_date__lte=self.start_date, end_date__gte=self.end_date)
            )

            return not conflicting_rents.exists()
        else:
            return True

    def save(self, *args, **kwargs):
        if self.rental_terms and self.period:
            if self.client.userprofile.premium:
                self.amount = self.rental_terms.premium_price * self.period
            else:
                self.amount = self.rental_terms.regular_price * self.period

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rental_terms} by {self.client}"

    @property
    def period(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return delta.days
        return 0
