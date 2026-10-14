from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Message(models.Model):
    """Un message échangé avec un contact (reçu ou envoyé)."""

    class Direction(models.TextChoices):
        INCOMING = "incoming", "Reçu"
        OUTGOING = "outgoing", "Envoyé"

    class Status(models.TextChoices):
        RECEIVED = "received", "Reçu"
        SENT = "sent", "Envoyé"
        FAILED = "failed", "Échec d'envoi"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    contact = models.ForeignKey(
        "contacts.Contact",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    direction = models.CharField(max_length=10, choices=Direction.choices)
    text = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.RECEIVED,
    )
    is_ai_generated = models.BooleanField(
        default=False,
        help_text="Vrai si le texte a été généré par l'IA.",
    )
    external_id = models.CharField(
        max_length=255,
        blank=True,
        help_text="Identifiant côté source (WhatsApp, notification...) pour éviter les doublons.",
    )
    sent_at = models.DateTimeField(
        default=timezone.now,
        help_text="Moment réel du message.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at", "id"]
        indexes = [
            models.Index(fields=["contact", "sent_at"], name="msg_contact_sent_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "external_id"],
                condition=~Q(external_id=""),
                name="unique_external_id_per_owner",
            )
        ]

    def __str__(self):
        preview = self.text[:30]
        return f"[{self.direction}] {self.contact.name}: {preview}"