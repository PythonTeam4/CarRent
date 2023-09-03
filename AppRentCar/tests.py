from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from .models import Rent, RentalTerms, Car, CompanyBranches


class RentCreateViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.car = Car.objects.create(
            brand="TestBrand",
            model="TestModel",
            cars_type="SomeType",
            capacity=1.58,
            year="2023",
            number_of_seats=4,
            consumption="SomeConsumption",
            power="SomePower",
            car_mileage="SomeMileage",
            transmission="SomeTransmission",
            no_gears="SomeGears",
            drive="SomeDrive",
        )
        self.rental_terms = RentalTerms.objects.create(car=self.car, price=100)
        self.company_branch = CompanyBranches.objects.create(city="TestCity")

        self.start_date = datetime(2023, 9, 1)
        self.end_date = datetime(2023, 9, 10)

    def test_car_available(self):
        rent = Rent(
            rental_terms=self.rental_terms,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        self.assertTrue(rent.is_car_available())

    def test_car_unavailable(self):
        company_branch = CompanyBranches.objects.create(city="Test City")
        Rent.objects.create(
            rental_terms=self.rental_terms,
            client=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            take_from=self.company_branch,
            take_back=self.company_branch,
        )
        rent = Rent(
            rental_terms=self.rental_terms,
            client=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            take_from=company_branch,
            take_back=company_branch,
        )

        self.rental_terms = RentalTerms.objects.create(car=self.car, price=100.00)
        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=5)

        self.assertFalse(rent.is_car_available())

    def test_rental_creation_when_proper_data(self):
        self.client.login(username="testuser", password="testpass")

        data = {
            "rental_terms": self.rental_terms.id,
            "start_date": "2023-09-01",
            "end_date": "2023-09-10",
            "take_from": self.company_branch.id,
            "take_back": self.company_branch.id,
        }

        response = self.client.post(
            reverse("create_rent", kwargs={"car_id": self.car.id}), data
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(Rent.objects.filter(rental_terms=self.rental_terms).exists())

    def test_form_invalid_data(self):
        self.client.login(username="testuser", password="testpass")

        data = {
            "rental_terms": self.rental_terms.id,
            "start_date": "2023-09-01",
            "end_date": "2023-09-10",
            "take_from": self.company_branch.id,
            "take_back": self.company_branch.id,
        }

        rent = Rent(
            rental_terms=self.rental_terms,
            client=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            take_from=self.company_branch,
            take_back=self.company_branch,
        )

        rent.save()

        response = self.client.post(
            reverse("create_rent", kwargs={"car_id": self.car.id}), data
        )

        self.rental_terms = RentalTerms.objects.create(car=self.car, price=100.00)
        self.start_date = timezone.now()
        self.end_date = self.start_date + timezone.timedelta(days=5)

        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Rent.objects.filter(rental_terms=self.rental_terms).exists())

    def test_form_validation_with_conflict(self):
        self.client.login(username="testuser", password="testpass")

        rent = Rent(
            rental_terms=self.rental_terms,
            client=self.user,
            start_date=self.start_date,
            end_date=self.end_date,
            take_from=self.company_branch,
            take_back=self.company_branch,
        )
        rent.save()

        data = {
            "rental_terms": self.rental_terms.id,
            "start_date": "2023-09-01",
            "end_date": "2023-09-10",
            "take_from": self.company_branch.id,
            "take_back": self.company_branch.id,
        }

        response = self.client.post(
            reverse("create_rent", kwargs={"car_id": self.car.id}), data
        )

        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Rent.objects.filter(rental_terms=self.rental_terms).exists())


class CarUpdateViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff_user = User.objects.create_user(
            username="staffuser", password="testpassword", is_staff=True
        )

        self.non_staff_user = User.objects.create_user(
            username="ordinaryuser", password="testpassword"
        )
        self.car = Car.objects.create(
            brand="Brand",
            model="Model",
            cars_type="Suv",
            engine="Benzyna",
            capacity=2.0,
            year="2023",
            number_of_seats=5,
            consumption="8L/100km",
            power="150KM",
            car_mileage="10 000 km",
            transmission="Automatyczna",
            no_gears="6",
            drive="Przedni",
        )

    def test_car_update_view_access_for_staff(self):
        self.client.login(username="staffuser", password="testpassword")

        response = self.client.get(reverse("cars_update", args=[self.car.pk]))

        self.assertEqual(response.status_code, 200)

    def test_car_update_view_access_for_non_staff(self):
        self.client.login(username="ordinaryuser", password="testpassword")

        response = self.client.get(reverse("cars_update", args=[self.car.pk]))

        self.assertEqual(response.status_code, 403)
