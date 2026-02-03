from django.urls import path, include
from rest_framework import routers

from core.views import (
    CrewViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    RouteViewSet
)

app_name = "core"

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]
