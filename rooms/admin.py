from django.contrib import admin
from django.utils.html import mark_safe
from . import models


class PhotoInline(admin.TabularInline):
    model = models.Photo


class RoomAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    inlines = (PhotoInline,)
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
        "count_photos",
        "total_rating",
        "get_photos",
    )
    raw_id_fields = ("host",)
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

    def count_photos(self, obj):
        return obj.photos.count()

    def get_photos(self, obj):
        photos = obj.photos.all()
        if photos:
            img_tags = []
            for photo in photos:
                img_tag = f'<a href="{photo.file.url}"><img height="50px" width="50px" src="{photo.file.url}"/></a>'
                img_tags.append(img_tag)
            return mark_safe("<br/>".join(img_tags))

    get_photos.short_description = "photos"


class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    def used_by(self, obj):
        return obj.rooms.count()

    list_display = ("name", "used_by")


class PhotoAdmin(admin.ModelAdmin):
    """Photo Admin Definition"""

    list_display = ("caption", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img height="50px" width="50px" src="{obj.file.url}"/>')

    get_thumbnail.short_description = "Thumbnail"


admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.RoomType, ItemAdmin)
admin.site.register(models.Amenity, ItemAdmin)
admin.site.register(models.Facility, ItemAdmin)
admin.site.register(models.HouseRule, ItemAdmin)
admin.site.register(models.Photo, PhotoAdmin)
