from django.contrib import admin

from core.models import (
    Flight,
    Crew,
    AirplaneType,
    Airplane,
    Airport,
    Route,
    Order,
    Ticket
)

admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Order)
admin.site.register(Flight)
admin.site.register(Ticket)


