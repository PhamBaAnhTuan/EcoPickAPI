from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet
from .models import Badge, UserBadge, ExchangItem
from .serializer import (
    BadgeSerializer,
    UserBadgeSerializer,
    ExchangeItemSerializer,
)
from .filter import BadgeFilter


class BadgeViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    filter_backends = [BadgeFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }

    # def get_queryset(self):
    #     user = self.request.user
    #     if not user or not user.is_authenticated:
    #         raise NotAuthenticated("You must be signin in to access this resource!")
    #     if not hasattr(user, "role") or user.role is None:
    #         raise PermissionDenied("You do not have a role assigned!")
    #     if user.role.name == "admin":
    #         return Post.objects.all()
    #     return Post.objects.filter(user_id=user.id)


class UserBadgeViewSet(BaseViewSet, OAuthLibMixin):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    filter_backends = [BadgeFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }


class ExchangeItemViewSet(BaseViewSet, OAuthLibMixin):
    queryset = ExchangItem.objects.all()
    serializer_class = ExchangeItemSerializer
    filter_backends = [BadgeFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }
