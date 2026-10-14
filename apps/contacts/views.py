from rest_framework import viewsets

from .models import Contact, RelationType
from .serializers import ContactSerializer, RelationTypeSerializer


class OwnedByUserMixin:
    """Chaque utilisateur ne voit et ne crée que ses propres données."""

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RelationTypeViewSet(OwnedByUserMixin, viewsets.ModelViewSet):
    queryset = RelationType.objects.all()
    serializer_class = RelationTypeSerializer


class ContactViewSet(OwnedByUserMixin, viewsets.ModelViewSet):
    queryset = Contact.objects.select_related("relation_type")
    serializer_class = ContactSerializer