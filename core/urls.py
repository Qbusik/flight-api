from django.urls import path, include
from rest_framework import routers

from core.views import (
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet,
    OrderViewSet,
    FlightViewSet
)

app_name = "core"

router = routers.DefaultRouter()
router.register("crew", CrewViewSet, basename="crew")
router.register("airplane_types", AirplaneTypeViewSet, basename="airplane_types")
router.register("airplanes", AirplaneViewSet, basename="airplanes")
router.register("airports", AirportViewSet, basename="airports")
router.register("routes", RouteViewSet, basename="routes")
router.register("orders", OrderViewSet, basename="orders")
router.register("flights", FlightViewSet, basename="flights")

urlpatterns = [path("", include(router.urls))]
