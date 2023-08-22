from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import Rent, RentalTerms, Car, CompanyBranches


class RentAvailabilityTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(
            brand='Brand',
            model='Model',
            cars_type='Suv',
            engine='Benzyna',
            capacity=2.0,
            year='2023',
            number_of_seats=5,
            consumption='8L/100km',
            power='150KM',
            car_mileage='10 000 km',
            transmission='Automatyczna',
            no_gears='6',
            drive='Przedni'
        )
        self.rental_terms = RentalTerms.objects.create(car=self.car, price=100.00)
        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=5)

    def test_car_available(self):
        rent = Rent(rental_terms=self.rental_terms, start_date=self.start_date, end_date=self.end_date)
        self.assertTrue(rent.is_car_available())

    def test_car_unavailable(self):
        company_branch = CompanyBranches.objects.create(city='Test City')
        Rent.objects.create(
            rental_terms=self.rental_terms,
            client=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            take_from=company_branch,
            take_back=company_branch,

        )
        rent = Rent(
            rental_terms=self.rental_terms,
            client=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            take_from=company_branch,
            take_back=company_branch,

        )
        self.assertFalse(rent.is_car_available())
