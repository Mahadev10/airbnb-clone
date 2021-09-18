from django.contrib import admin
from . import models


class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""

    pass


admin.site.register(models.Reservation, ReservationAdmin)
