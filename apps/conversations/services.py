from django.db import IntegrityError, transaction

from .models import Message


def record_message(
    *,
    owner,
    contact,
    direction,
    text,
    external_id="",
    is_ai_generated=False,
    status=None,
    sent_at=None,
):
    """
    Enregistre un message. Retourne (message, created).

    Si external_id est fourni et existe déjà pour cet utilisateur,
    retourne le message existant sans en créer un second (anti-doublon).
    """
    if contact.owner_id != owner.pk:
        raise ValueError("Ce contact n'appartient pas à cet utilisateur.")

    if external_id:
        existing = Message.objects.filter(owner=owner, external_id=external_id).first()
        if existing:
            return existing, False

    if status is None:
        status = (
            Message.Status.RECEIVED
            if direction == Message.Direction.INCOMING
            else Message.Status.SENT
        )

    data = {
        "owner": owner,
        "contact": contact,
        "direction": direction,
        "text": text,
        "status": status,
        "is_ai_generated": is_ai_generated,
        "external_id": external_id,
    }
    if sent_at is not None:
        data["sent_at"] = sent_at

    try:
        with transaction.atomic():
            message = Message.objects.create(**data)
    except IntegrityError:
        # Deux requêtes simultanées avec le même external_id
        if external_id:
            existing = Message.objects.filter(
                owner=owner, external_id=external_id
            ).first()
            if existing:
                return existing, False
        raise

    return message, True


def get_recent_messages(contact, limit=5):
    """Les derniers messages d'un contact, du plus ancien au plus récent."""
    latest = Message.objects.filter(contact=contact).order_by("-sent_at", "-id")[:limit]
    return list(reversed(latest))