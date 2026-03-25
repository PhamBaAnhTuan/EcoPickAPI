from .views import ConversationViewSet, ConversationMemberViewSet, MessageViewSet, PointLogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet)
router.register(r"conversation-members", ConversationMemberViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"point-logs", PointLogViewSet)

urlpatterns = router.urls
