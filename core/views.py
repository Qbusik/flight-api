from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from core.models import Crew
from core.serializers import CrewSerializer


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
