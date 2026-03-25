from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet

from app.views.base import BaseViewSet
from .models import Conversation, ConversationMember, Message, PointLog
from .serializer import (
    ConversationSerializer,
    ConversationMemberSerializer,
    MessageSerializer,
    PointLogSerializer,
)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


class ConversationViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
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


class ConversationMemberViewSet(BaseViewSet, OAuthLibMixin):
    queryset = ConversationMember.objects.all()
    serializer_class = ConversationMemberSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }


class MessageViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }


class PointLogViewSet(BaseViewSet, OAuthLibMixin):
    queryset = PointLog.objects.all()
    serializer_class = PointLogSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }
