from django.urls import path, include
from rest_framework import routers

from core.views import CrewViewSet

app_name = "core"

router = routers.DefaultRouter()
router.register("crew", CrewViewSet)

urlpatterns = [path("", include(router.urls))]