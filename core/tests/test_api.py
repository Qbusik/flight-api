from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    AirplaneType,
    Crew,
    Airport,
    Route,
    Airplane,
    Flight,
    Order
)
from user.models import User


AIRPLANE_TYPES_URL = reverse("core:airplane_types-list")
AIRPLANES_URL = reverse("core:airplanes-list")
CREW_URL = reverse("core:crew-list")
AIRPORTS_URL = reverse("core:airports-list")
ROUTES_URL = reverse("core:routes-list")
ORDERS_URL = reverse("core:orders-list")
FLIGHTS_URL = reverse("core:flights-list")


def sample_airplane_type(**params):
    defaults = {
        "name": "Test-type",
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {
        "name": "Test-type",
        "rows": 10,
        "seats_in_row": 10,
        "airplane_type": airplane_type
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "Test-First",
        "last_name": "Test-Last",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "Test-Airport",
        "closest_big_city": "Test-City"
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name="Test-Source", closest_big_city="Test-CitySource")
    destination = sample_airport(name="Test-Destination", closest_big_city="Test-CityDestination")
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 999,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    departure = timezone.now()
    arrival = departure + timedelta(hours=2)
    crew = sample_crew()
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": departure,
        "arrival_time": arrival,
    }
    defaults.update(params)
    flight = Flight.objects.create(**defaults)
    flight.crew.set([crew])
    return flight


class UnauthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        urls = {
            AIRPLANE_TYPES_URL,
            AIRPLANES_URL,
            CREW_URL,
            AIRPORTS_URL,
            ROUTES_URL,
            ORDERS_URL,
            FLIGHTS_URL
        }
        for url in urls:
            res = self.client.get(url)
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test1password123",
        )
        self.client.force_authenticate(self.user)

    def test_airplane_types(self):
        res = self.client.post(AIRPLANE_TYPES_URL, {"name": "Test-type"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(AIRPLANE_TYPES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_airplanes(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Test-type",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type.id
        }
        res = self.client.post(AIRPLANES_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(AIRPLANES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_crew(self):
        res = self.client.post(CREW_URL, {"first_name": "Test-first", "last_name": "Test-last"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_airports(self):
        res = self.client.post(AIRPORTS_URL, {"name": "Test", "closest_big_city": "TestCity"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(AIRPORTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_routes(self):
        source_airport = sample_airport()
        destination_airport = sample_airport()
        payload = {
            "source": source_airport.id,
            "destination": destination_airport.id,
            "distance": 999,
        }

        res = self.client.post(ROUTES_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(ROUTES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_flights(self):
        airplane = sample_airplane()
        route = sample_route()
        crew = sample_crew()
        departure = timezone.now()
        arrival = departure + timedelta(hours=2)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew": [crew.id]
        }

        res = self.client.post(FLIGHTS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        res = self.client.get(FLIGHTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_orders(self):
        flight = sample_flight()
        payload = {
            "tickets": [
                {
                    "row": 11,
                    "seat": 1,
                    "flight": flight.id
                }
            ]
        }

        res = self.client.post(ORDERS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 11,
                    "flight": flight.id
                }
            ]
        }

        res = self.client.post(ORDERS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.id
                }
            ]
        }

        res = self.client.post(ORDERS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(ORDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

        res = self.client.post(ORDERS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.user = get_user_model().objects.create_user(
            "test2@test2.com",
            "test1password321",
        )
        self.client.force_authenticate(self.user)

        res = self.client.get(ORDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 0)


class AdminUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="adminpassword"
        )
        self.client.force_authenticate(self.admin_user)

    def test_airplane_types(self):
        res = self.client.post(AIRPLANE_TYPES_URL, {"name": "Test-type"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_airplanes(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Test-type",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type.id
        }
        res = self.client.post(AIRPLANES_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_crew(self):
        res = self.client.post(CREW_URL, {"first_name": "Test-first", "last_name": "Test-last"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_airports(self):
        res = self.client.post(AIRPORTS_URL, {"name": "Test", "closest_big_city": "TestCity"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_routes(self):
        source_airport = sample_airport()
        destination_airport = sample_airport()
        payload = {
            "source": source_airport.id,
            "destination": destination_airport.id,
            "distance": 999,
        }

        res = self.client.post(ROUTES_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_flights(self):
        airplane = sample_airplane()
        route = sample_route()
        crew = sample_crew()
        departure = timezone.now()
        arrival = departure + timedelta(hours=2)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew": [crew.id]
        }

        res = self.client.post(FLIGHTS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure,
            "arrival_time": departure,
            "crew": [crew.id]
        }

        res = self.client.post(FLIGHTS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": arrival,
            "arrival_time": departure,
            "crew": [crew.id]
        }

        res = self.client.post(FLIGHTS_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
