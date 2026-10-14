from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("contact", "direction", "short_text", "status", "is_ai_generated", "sent_at")
    list_filter = ("direction", "status", "is_ai_generated")
    search_fields = ("text", "contact__name", "contact__phone_number")
    date_hierarchy = "sent_at"

    @admin.display(description="Texte")
    def short_text(self, obj):
        return obj.text[:50]