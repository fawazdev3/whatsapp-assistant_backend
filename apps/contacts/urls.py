from rest_framework.routers import SimpleRouter

from .views import ContactViewSet, RelationTypeViewSet

router = SimpleRouter()
router.register("relation-types", RelationTypeViewSet, basename="relation-type")
router.register("contacts", ContactViewSet, basename="contact")

urlpatterns = router.urls