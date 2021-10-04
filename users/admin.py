from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
        "get_avatar",
    )
    list_filter = UserAdmin.list_filter + ("superhost",)

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(
                f'<img height="50px" width="50px" src="{obj.avatar.url}"/>'
            )
        return ""

    get_avatar.short_description = "Avatar"


admin.site.register(User, CustomUserAdmin)
