from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Message
from .serializers import MessageSerializer


class MessagePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class MessageViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Consultation et suppression de l'historique.
    Filtre possible : /api/messages/?contact=3
    Les messages les plus récents viennent en premier.
    """

    serializer_class = MessageSerializer
    pagination_class = MessagePagination

    def get_queryset(self):
        queryset = Message.objects.filter(owner=self.request.user).select_related(
            "contact"
        )
        contact_id = self.request.query_params.get("contact")
        if contact_id and contact_id.isdigit():
            queryset = queryset.filter(contact_id=int(contact_id))
        return queryset.order_by("-sent_at", "-id")