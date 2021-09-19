from django.contrib import admin
from . import models


class ReviewAdmin(admin.ModelAdmin):
    """Review Admin Definition"""

    list_display=("__str__","user","rating_average")


admin.site.register(models.Review, ReviewAdmin)
