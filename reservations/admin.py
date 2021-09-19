from django.contrib import admin
from . import models


class ReservationAdmin(admin.ModelAdmin):
    """Reservation Admin Definition"""

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )
    list_filter = ("status",)


admin.site.register(models.Reservation, ReservationAdmin)
