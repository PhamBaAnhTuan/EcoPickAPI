from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet

from app.views.base import BaseViewSet
from .models import Event, EventParticipants, TourStop
from .serializer import (
    EventSerializer,
    EventParticipantsSerializer,
    TourStopSerializer,
)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


class EventViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
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


class EventParticipantsViewSet(BaseViewSet, OAuthLibMixin):
    queryset = EventParticipants.objects.all()
    serializer_class = EventParticipantsSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }


class TourStopViewSet(BaseViewSet, OAuthLibMixin):
    queryset = TourStop.objects.all()
    serializer_class = TourStopSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }
