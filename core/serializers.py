from rest_framework import serializers

from core.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Order,
    Ticket, Flight
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


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
    route = RouteListSerializer(many=False, read_only=True)
    airplane = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "created_at", "user")


class OrderListSerializer(OrderSerializer):
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )
    num_of_tickets = serializers.IntegerField(source="tickets.count", read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "num_of_tickets")


class OrderRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="email"
    )
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "tickets")
