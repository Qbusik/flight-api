from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Order,
    Ticket,
    Flight
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class CrewShortSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Crew
        fields = ("id", "full_name")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "capacity", "airplane_type")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def validate(self, attrs):
        if attrs["source"] == attrs["destination"]:
            raise serializers.ValidationError(
                "Source and destination must be different"
            )
        return attrs


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.CharField(source="source.name")
    destination = serializers.CharField(source="destination.name")
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")

    def validate(self, attrs):
        if attrs["arrival_time"] <= attrs["departure_time"]:
            raise serializers.ValidationError(
                "Arrival time cannot be earlier than departure time"
            )
        return attrs


class FlightListSerializer(serializers.ModelSerializer):
    route = RouteListSerializer(
        many=False, read_only=True
    )
    airplane = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "tickets_available")


class FlightRetrieveSerializer(FlightListSerializer):
    crew = CrewShortSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class TicketCreateSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(
        queryset=Flight.objects.all()
    )

    def validate(self, attrs):
        data = super(TicketCreateSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketWithFlightExposedSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            user = self.context['request'].user
            order = Order.objects.create(user=user, **validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )
    num_of_tickets = serializers.IntegerField(
        source="tickets.count", read_only=True
    )

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "num_of_tickets")


class OrderRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )
    tickets = TicketWithFlightExposedSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")


class FlightInCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class CrewRetrieveSerializer(serializers.ModelSerializer):
    flights = FlightInCrewSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "flights")
