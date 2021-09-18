from django.contrib import admin
from . import models


class RoomAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    pass


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
