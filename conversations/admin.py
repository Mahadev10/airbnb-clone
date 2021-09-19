from django.contrib import admin
from . import models


class ConversationAdmin(admin.ModelAdmin):
    """Conversation Admin Definition"""

    list_display = (
        "__str__",
        "created",
        "count_messages",
        "count_participants",
    )


class MessageAdmin(admin.ModelAdmin):
    """Message Admin Definition"""

    pass


admin.site.register(models.Conversation, ConversationAdmin)
admin.site.register(models.Message, MessageAdmin)
