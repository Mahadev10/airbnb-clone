from core import models
from django.contrib import admin
from .models import List


class ListAdmin(admin.ModelAdmin):
    """List Admin Definition"""
    pass
admin.site.register(List,ListAdmin)