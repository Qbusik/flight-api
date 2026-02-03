from django.urls import path, include
from rest_framework import routers

from core.views import (
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet
)

app_name = "core"

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airport", AirportViewSet)

urlpatterns = [path("", include(router.urls))]
