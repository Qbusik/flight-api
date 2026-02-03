from rest_framework.viewsets import ModelViewSet

from core.models import (
    Crew,
    AirplaneType,
    Airplane, Airport
)
from core.serializers import (
    CrewSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    AirportSerializer
)


class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.prefetch_related("airplane_type")
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "post":
            return AirplaneSerializer

        if self.action == "retrieve":
            return AirplaneListSerializer

        if self.action == "update":
            return AirplaneSerializer

        return AirplaneSerializer


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
