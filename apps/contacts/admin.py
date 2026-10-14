from django.contrib import admin

from .models import Contact, RelationType


@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "formality", "address_form", "default_autonomy")
    list_filter = ("formality", "default_autonomy")
    search_fields = ("name",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "relation_type", "autonomy", "owner")
    list_filter = ("relation_type", "autonomy")
    search_fields = ("name", "phone_number")