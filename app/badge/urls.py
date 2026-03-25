from .views import BadgeViewSet, UserBadgeViewSet ,ExchangeItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"badges", BadgeViewSet)
router.register(r"user-badges", UserBadgeViewSet)
router.register(r"exchange-items", ExchangeItemViewSet)

urlpatterns = router.urls
