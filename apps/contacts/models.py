from django.conf import settings
from django.db import models


class Autonomy(models.TextChoices):
    """Niveau d'autonomie de l'assistant pour répondre."""

    AUTO = "auto", "Automatique"
    DRAFT = "draft", "Brouillon à valider"
    DISABLED = "disabled", "Désactivé"


class RelationType(models.Model):
    """Type de relation : grand-mère, cousin, collègue... (extensible librement)."""

    class Formality(models.TextChoices):
        CASUAL = "casual", "Décontracté"
        RESPECTFUL = "respectful", "Respectueux"
        FORMAL = "formal", "Formel"

    class AddressForm(models.TextChoices):
        TU = "tu", "Tutoiement"
        VOUS = "vous", "Vouvoiement"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="relation_types",
    )
    name = models.CharField(max_length=100)
    formality = models.CharField(
        max_length=20,
        choices=Formality.choices,
        default=Formality.CASUAL,
    )
    address_form = models.CharField(
        max_length=10,
        choices=AddressForm.choices,
        default=AddressForm.TU,
    )
    guidelines = models.TextField(
        blank=True,
        help_text="Consignes générales pour l'IA (ton, sujets, expressions...).",
    )
    default_autonomy = models.CharField(
        max_length=20,
        choices=Autonomy.choices,
        default=Autonomy.DRAFT,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_relation_name_per_owner",
            )
        ]

    def __str__(self):
        return self.name


class Contact(models.Model):
    """Une personne avec qui tu échanges."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    name = models.CharField(max_length=150)
    phone_number = models.CharField(
        max_length=20,
        help_text="Format international, ex: +22890000000",
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
    )
    autonomy = models.CharField(
        max_length=20,
        choices=Autonomy.choices,
        blank=True,
        help_text="Vide = utilise le réglage du type de relation.",
    )
    personal_notes = models.TextField(
        blank=True,
        help_text="Détails propres à cette personne (langue, sujets, ce qu'elle déteste...).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "phone_number"],
                name="unique_phone_per_owner",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    @property
    def effective_autonomy(self):
        """Réglage du contact, sinon celui de sa relation, sinon brouillon par sécurité."""
        if self.autonomy:
            return self.autonomy
        if self.relation_type:
            return self.relation_type.default_autonomy
        return Autonomy.DRAFT