from rest_framework import serializers

from .models import Contact, RelationType
from .services import is_valid_phone_number, normalize_phone_number


class RelationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationType
        fields = [
            "id",
            "name",
            "formality",
            "address_form",
            "guidelines",
            "default_autonomy",
        ]

    def validate_name(self, value):
        value = value.strip()
        user = self.context["request"].user
        duplicates = RelationType.objects.filter(owner=user, name__iexact=value)
        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise serializers.ValidationError(
                "Tu as déjà un type de relation avec ce nom."
            )
        return value


class ContactSerializer(serializers.ModelSerializer):
    effective_autonomy = serializers.CharField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "phone_number",
            "relation_type",
            "autonomy",
            "effective_autonomy",
            "personal_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_fields(self):
        """Limite relation_type aux types de relation de l'utilisateur connecté."""
        fields = super().get_fields()
        request = self.context.get("request")
        if request is not None and request.user.is_authenticated:
            queryset = RelationType.objects.filter(owner=request.user)
        else:
            queryset = RelationType.objects.none()
        fields["relation_type"].queryset = queryset
        return fields

    def validate_phone_number(self, value):
        value = value.strip()
        if not value.startswith(("+", "00")):
            raise serializers.ValidationError(
                "Utilise le format international, ex : +22890000000."
            )
        normalized = normalize_phone_number(value)
        if not is_valid_phone_number(normalized):
            raise serializers.ValidationError(
                "Numéro invalide. Exemple valide : +22890000000."
            )

        user = self.context["request"].user
        duplicates = Contact.objects.filter(owner=user, phone_number=normalized)
        if self.instance:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if duplicates.exists():
            raise serializers.ValidationError(
                "Tu as déjà un contact avec ce numéro."
            )
        return normalized