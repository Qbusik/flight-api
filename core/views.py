from django.db.models import F, Count, Prefetch
from rest_framework.viewsets import ModelViewSet

from core.models import (
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Order, Flight, Ticket
)
from core.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    OrderSerializer,
    OrderListSerializer,
    OrderRetrieveSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer
)


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer

        return AirplaneSerializer


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RouteListSerializer

        return RouteSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        if self.action == "retrieve":
            return OrderRetrieveSerializer

        return OrderSerializer

    def get_queryset(self):
        return (
            Order.objects
            .select_related("user")
            .prefetch_related(
                Prefetch(
                    "tickets",
                    queryset=Ticket.objects.select_related(
                        "flight",
                        "flight__route",
                        "flight__route__source",
                        "flight__route__destination",
                        "flight__airplane",
                    )
                )
            )
            .filter(user=self.request.user)
        )


class FlightViewSet(ModelViewSet):
    queryset = Flight.objects.select_related(
        "route", "airplane", "route__source", "route__destination",
    ).prefetch_related(
        "crew",
    ).annotate(
        tickets_available=(
            F("airplane__rows") * F("airplane__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightRetrieveSerializer
        return FlightSerializer
