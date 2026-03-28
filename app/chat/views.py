from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet
from .models import Conversation, ConversationMember, Message, PointLog
from .serializer import (
    ConversationSerializer,
    ConversationMemberSerializer,
    MessageSerializer,
    PointLogSerializer,
)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from app.swagger import common_list_params


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách cuộc hội thoại",
        description="Lấy tất cả cuộc hội thoại.",
        parameters=common_list_params,
        tags=["Conversation"],
    ),
    retrieve=extend_schema(summary="Chi tiết cuộc hội thoại", tags=["Conversation"]),
    create=extend_schema(
        summary="Tạo cuộc hội thoại mới",
        description="Tạo cuộc hội thoại mới.\n\n**Body fields:** type (one_on_one/group), event_id (UUID FK, optional), name",
        tags=["Conversation"],
    ),
    update=extend_schema(summary="Cập nhật cuộc hội thoại", tags=["Conversation"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Conversation"]),
    destroy=extend_schema(summary="Xóa cuộc hội thoại", tags=["Conversation"]),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách thành viên hội thoại",
        description="Lấy tất cả thành viên trong các cuộc hội thoại.",
        parameters=common_list_params,
        tags=["Conversation Member"],
    ),
    retrieve=extend_schema(summary="Chi tiết thành viên", tags=["Conversation Member"]),
    create=extend_schema(
        summary="Thêm thành viên",
        description="Thêm user vào cuộc hội thoại.\n\n**Body fields:** conversation_id (UUID FK), user_id (UUID FK), last_read_at (datetime, optional)",
        tags=["Conversation Member"],
    ),
    update=extend_schema(summary="Cập nhật thành viên", tags=["Conversation Member"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Conversation Member"]),
    destroy=extend_schema(summary="Xóa thành viên", tags=["Conversation Member"]),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách tin nhắn",
        description="Lấy tất cả tin nhắn.",
        parameters=common_list_params,
        tags=["Message"],
    ),
    retrieve=extend_schema(summary="Chi tiết tin nhắn", tags=["Message"]),
    create=extend_schema(
        summary="Gửi tin nhắn",
        description="Gửi tin nhắn trong cuộc hội thoại.\n\n**Body fields:** conversation_id (UUID FK), sender_id (UUID FK), content, photo_url, location_latitude (float), location_longitude (float)",
        tags=["Message"],
    ),
    update=extend_schema(summary="Cập nhật tin nhắn", tags=["Message"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Message"]),
    destroy=extend_schema(summary="Xóa tin nhắn", tags=["Message"]),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="Lịch sử điểm eco",
        description="Lấy tất cả log điểm eco của user.",
        parameters=common_list_params,
        tags=["Point Log"],
    ),
    retrieve=extend_schema(summary="Chi tiết log điểm", tags=["Point Log"]),
    create=extend_schema(
        summary="Tạo log điểm",
        description="Ghi nhận thay đổi điểm eco.\n\n**Body fields:** user_id (UUID FK), points (int), reason (report_created/event_completed/reward_redeemed/...)",
        tags=["Point Log"],
    ),
    update=extend_schema(summary="Cập nhật log điểm", tags=["Point Log"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Point Log"]),
    destroy=extend_schema(summary="Xóa log điểm", tags=["Point Log"]),
)
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
