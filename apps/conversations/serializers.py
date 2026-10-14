from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source="contact.name", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "contact",
            "contact_name",
            "direction",
            "text",
            "status",
            "is_ai_generated",
            "sent_at",
        ]
        read_only_fields = fields