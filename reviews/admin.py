from django.contrib import admin
from . import models


class ReviewAdmin(admin.ModelAdmin):
    """Review Admin Definition"""

    pass


admin.site.register(models.Review, ReviewAdmin)
