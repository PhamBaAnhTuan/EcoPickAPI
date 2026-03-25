from .views import EventViewSet, EventParticipantsViewSet, TourStopViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"event-participants", EventParticipantsViewSet)
router.register(r"tour-stops", TourStopViewSet)

urlpatterns = router.urls
