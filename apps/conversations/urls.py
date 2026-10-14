from rest_framework.routers import SimpleRouter

from .views import MessageViewSet

router = SimpleRouter()
router.register("messages", MessageViewSet, basename="message")

urlpatterns = router.urls