from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
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
)


AIRPLANE_TYPES_URL = reverse("core:airplane_types-list")
AIRPLANES_URL = reverse("core:airplanes-list")
CREW_URL = reverse("core:crew-list")
AIRPORTS_URL = reverse("core:airports-list")
ROUTES_URL = reverse("core:routes-list")
ORDERS_URL = reverse("core:orders-list")
FLIGHTS_URL = reverse("core:flights-list")


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        email="test@test.com",
        password="test1password123"
    )


@pytest.fixture
def another_user(db):
    return get_user_model().objects.create_user(
        email="test2@test2.com",
        password="test1password321"
    )


@pytest.fixture
def admin_user(db):
    return get_user_model().objects.create_superuser(
        email="admin@admin.com",
        password="test1admin123"
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(admin_user)
    return client


@pytest.fixture
def airplane_type_factory(db):
    def create(**params):
        defaults = {"name": "Test-type"}
        defaults.update(params)
        return AirplaneType.objects.create(**defaults)
    return create


@pytest.fixture
def airplane_factory(db, airplane_type_factory):
    def create(**params):
        airplane_type = params.pop("airplane_type", airplane_type_factory())
        defaults = {
            "name": "Test-type",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type
        }
        defaults.update(params)
        return Airplane.objects.create(**defaults)
    return create


@pytest.fixture
def crew_factory(db):
    def create(**params):
        defaults = {
            "first_name": "Test-First",
            "last_name": "Test-Last",
        }
        defaults.update(params)
        return Crew.objects.create(**defaults)
    return create


@pytest.fixture
def airport_factory(db):
    def create(**params):
        defaults = {
            "name": "Test-Airport",
            "closest_big_city": "Test-City"
        }
        defaults.update(params)
        return Airport.objects.create(**defaults)
    return create


@pytest.fixture
def route_factory(db, airport_factory):
    def create(**params):
        source = params.pop("source", airport_factory())
        destination = params.pop("destination", airport_factory(name="Test-Airport2", closest_big_city="Test-City2"))
        defaults = {
            "source": source,
            "destination": destination,
            "distance": 999,
        }
        defaults.update(params)
        return Route.objects.create(**defaults)
    return create


@pytest.fixture
def flight_factory(db, route_factory, airplane_factory, crew_factory):
    def create(**params):
        route = params.pop("route", route_factory())
        airplane = params.pop("airplane", airplane_factory())
        departure = timezone.now()
        arrival = departure + timedelta(hours=2)
        crews = params.pop("crew", [crew_factory()])
        defaults = {
            "route": route,
            "airplane": airplane,
            "departure_time": departure,
            "arrival_time": arrival,
        }
        defaults.update(params)
        flight = Flight.objects.create(**defaults)
        flight.crew.set(crews)
        return flight
    return create


class TestUnauthenticatedUser:
    def test_auth_required(self):
        client = APIClient()

        urls = [
            AIRPLANE_TYPES_URL,
            AIRPLANES_URL,
            CREW_URL,
            AIRPORTS_URL,
            ROUTES_URL,
            ORDERS_URL,
            FLIGHTS_URL
        ]

        for url in urls:
            res = client.get(url)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED


class TestAuthenticatedUserTests:
    def test_airplane_types(self, auth_client):
        res = auth_client.post(AIRPLANE_TYPES_URL, {"name": "Test-type"}, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = auth_client.get(AIRPLANE_TYPES_URL)
        assert res.status_code == status.HTTP_200_OK

    def test_airplanes(self, auth_client, airplane_type_factory):
        airplane_type = airplane_type_factory()
        payload = {
            "name": "Test-type",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type.id
        }
        res = auth_client.post(AIRPLANES_URL, payload, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = auth_client.get(AIRPLANES_URL)
        assert res.status_code == status.HTTP_200_OK

    def test_crew(self, auth_client):
        res = auth_client.post(CREW_URL, {"first_name": "Test-first", "last_name": "Test-last"}, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = auth_client.get(CREW_URL)
        assert res.status_code == status.HTTP_200_OK

    def test_airports(self, auth_client):
        res = auth_client.post(AIRPORTS_URL, {"name": "Test", "closest_big_city": "TestCity"}, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = auth_client.get(AIRPORTS_URL)
        assert res.status_code == status.HTTP_200_OK

    def test_routes(self, auth_client, airport_factory):
        source_airport = airport_factory()
        destination_airport = airport_factory(name="Test22", closest_big_city="TestCity22")
        payload = {
            "source": source_airport.id,
            "destination": destination_airport.id,
            "distance": 999,
        }
        res = auth_client.post(ROUTES_URL, payload, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = auth_client.get(ROUTES_URL)
        assert res.status_code == status.HTTP_200_OK

    def test_flights(self, auth_client, airplane_factory, route_factory, crew_factory):
        airplane = airplane_factory()
        route = route_factory()
        crew = crew_factory()
        departure = timezone.now()
        arrival = departure + timedelta(hours=2)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew": [crew.id]
        }

        res = auth_client.post(FLIGHTS_URL, payload, format="json")
        assert res.status_code == status.HTTP_403_FORBIDDEN

        res = auth_client.get(FLIGHTS_URL)
        assert res.status_code == status.HTTP_200_OK

    def test_orders(self, auth_client, another_user, flight_factory):
        flight = flight_factory()
        payload = {
            "tickets": [
                {
                    "row": 11,
                    "seat": 1,
                    "flight": flight.id
                }
            ]
        }

        res = auth_client.post(ORDERS_URL, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 11,
                    "flight": flight.id
                }
            ]
        }

        res = auth_client.post(ORDERS_URL, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "flight": flight.id
                }
            ]
        }

        res = auth_client.post(ORDERS_URL, payload, format="json")
        assert res.status_code == status.HTTP_201_CREATED

        res = auth_client.get(ORDERS_URL)
        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 1

        res = auth_client.post(ORDERS_URL, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        auth_client.force_authenticate(another_user)

        res = auth_client.get(ORDERS_URL)
        assert res.status_code == status.HTTP_200_OK
        assert res.data['count'] == 0


class TestAdminUser:
    def test_airplane_types(self, admin_client):
        res = admin_client.post(AIRPLANE_TYPES_URL, {"name": "Test-type"}, format="json")
        assert res.status_code == status.HTTP_201_CREATED

    def test_airplanes(self, admin_client, airplane_type_factory):
        airplane_type = airplane_type_factory()
        payload = {
            "name": "Test-type",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": airplane_type.id
        }
        res = admin_client.post(AIRPLANES_URL, payload, format="json")
        assert res.status_code == status.HTTP_201_CREATED

    def test_crew(self, admin_client):
        res = admin_client.post(CREW_URL, {"first_name": "Test-first", "last_name": "Test-last"}, format="json")
        assert res.status_code == status.HTTP_201_CREATED

    def test_airports(self, admin_client):
        res = admin_client.post(AIRPORTS_URL, {"name": "Test", "closest_big_city": "TestCity"}, format="json")
        assert res.status_code == status.HTTP_201_CREATED

    def test_routes(self, admin_client, airport_factory):
        source_airport = airport_factory()
        destination_airport = airport_factory(name="Test2", closest_big_city="TestCity2")
        payload = {
            "source": source_airport.id,
            "destination": destination_airport.id,
            "distance": 999,
        }

        res = admin_client.post(ROUTES_URL, payload, format="json")
        assert res.status_code == status.HTTP_201_CREATED

        payload = {
            "source": source_airport.id,
            "destination": source_airport.id,
            "distance": 999,
        }

        res = admin_client.post(ROUTES_URL, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_flights(self, admin_client, airplane_factory, route_factory, crew_factory):
        airplane = airplane_factory()
        route = route_factory()
        crew = crew_factory()
        departure = timezone.now()
        arrival = departure + timedelta(hours=2)
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew": [crew.id]
        }

        res = admin_client.post(FLIGHTS_URL, payload, format="json")
        assert res.status_code == status.HTTP_201_CREATED

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": departure,
            "arrival_time": departure,
            "crew": [crew.id]
        }

        res = admin_client.post(FLIGHTS_URL, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": arrival,
            "arrival_time": departure,
            "crew": [crew.id]
        }

        res = admin_client.post(FLIGHTS_URL, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
