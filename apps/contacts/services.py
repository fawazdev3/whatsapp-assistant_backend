import re

from .models import Contact

PHONE_PATTERN = re.compile(r"^\+\d{8,15}$")


def normalize_phone_number(raw):
    """
    Met un numéro au format +XXXXXXXXXXX (chiffres uniquement après le +).

    Accepte "+228 90 00 00 00", "00228 90-00-00-00" ou "22890000000"
    (ce dernier est le format envoyé par l'API WhatsApp Cloud).
    """
    cleaned = re.sub(r"[^\d+]", "", raw or "")
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    elif not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    return cleaned


def is_valid_phone_number(normalized):
    return bool(PHONE_PATTERN.match(normalized))


def get_contact_by_phone(owner, phone_number):
    """Retourne le Contact de cet utilisateur ayant ce numéro, ou None."""
    normalized = normalize_phone_number(phone_number)
    return (
        Contact.objects.select_related("relation_type")
        .filter(owner=owner, phone_number=normalized)
        .first()
    )