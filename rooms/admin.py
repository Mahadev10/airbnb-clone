from django.contrib import admin
from . import models


class RoomAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                ),
            },
        ),
        (
            "Times",
            {
                "fields": (
                    "check_in",
                    "check_out",
                    "instant_book",
                ),
            },
        ),
        (
            "Spaces",
            {
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                ),
            },
        ),
        (
            "More About The Space",
            {
                "classes": ("collapse",),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
        (
            "Last Details",
            {
                "fields": ("host",),
            },
        ),
    )
    list_display = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "host",
        "count_amenities",
    )
    ordering = ("name", "price", "bedrooms")
    list_filter = (
        "instant_book",
        "host__superhost",
        "host__gender",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )
    search_fields = (
        "=city",
        "^host__username",
    )
    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()


class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    pass


class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    pass


admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.RoomType, ItemAdmin)
admin.site.register(models.Amenity, ItemAdmin)
admin.site.register(models.Facility, ItemAdmin)
admin.site.register(models.HouseRule, ItemAdmin)
admin.site.register(models.Photo, PhotoAdmin)
