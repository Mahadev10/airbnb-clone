from core import models
from django.contrib import admin
from .models import List


class ListAdmin(admin.ModelAdmin):
    """List Admin Definition"""

    list_display = (
        "name",
        "user",
        "count_rooms",
    )
    search_fields = ("name",)
    filter_horizontal = ("rooms",)


admin.site.register(List, ListAdmin)
