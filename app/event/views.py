from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet
from .models import Event, EventParticipants, TourStop
from .serializer import (
    EventSerializer,
    EventParticipantsSerializer,
    TourStopSerializer,
)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from app.swagger import common_list_params


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách sự kiện",
        description="Lấy tất cả sự kiện môi trường. Hỗ trợ tìm kiếm textSearch và phân trang limitnumber.",
        parameters=common_list_params,
        tags=["Event"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết sự kiện",
        description="Lấy thông tin chi tiết 1 sự kiện theo UUID.",
        tags=["Event"],
    ),
    create=extend_schema(
        summary="Tạo sự kiện mới",
        description="Tạo sự kiện mới. Chỉ admin có quyền.\n\n**Body fields:** organizer_id, title, description, cover_image_url, type (cleanup/tree_planting/workshop/beach_cleanup/education/tour), start_date, end_date, latitude, longitude, location, address, max_paticipants, equipment, difficulty (easy/medium/hard), eco_point_reward, status (upcoming/ongoing/completed/cancelled)",
        tags=["Event"],
    ),
    update=extend_schema(
        summary="Cập nhật sự kiện",
        description="Cập nhật thông tin sự kiện (partial update).",
        tags=["Event"],
    ),
    partial_update=extend_schema(
        summary="Cập nhật một phần sự kiện",
        tags=["Event"],
    ),
    destroy=extend_schema(
        summary="Xóa sự kiện",
        description="Xóa sự kiện. Chỉ admin có quyền.",
        tags=["Event"],
    ),
)
class EventViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách người tham gia",
        description="Lấy tất cả người tham gia sự kiện.",
        parameters=common_list_params,
        tags=["Event Participant"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết người tham gia",
        tags=["Event Participant"],
    ),
    create=extend_schema(
        summary="Thêm người tham gia",
        description="Đăng ký tham gia sự kiện.\n\n**Body fields:** event_id (UUID), user_id (UUID), status (joined/checked_in/completed/left/cancelled)",
        tags=["Event Participant"],
    ),
    update=extend_schema(
        summary="Cập nhật trạng thái tham gia",
        tags=["Event Participant"],
    ),
    partial_update=extend_schema(
        summary="Cập nhật một phần",
        tags=["Event Participant"],
    ),
    destroy=extend_schema(
        summary="Xóa người tham gia",
        tags=["Event Participant"],
    ),
)
class EventParticipantsViewSet(BaseViewSet, OAuthLibMixin):
    queryset = EventParticipants.objects.all()
    serializer_class = EventParticipantsSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách điểm dừng tour",
        description="Lấy tất cả điểm dừng của một tour/sự kiện.",
        parameters=common_list_params,
        tags=["Tour Stop"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết điểm dừng",
        tags=["Tour Stop"],
    ),
    create=extend_schema(
        summary="Tạo điểm dừng mới",
        description="Thêm điểm dừng cho sự kiện tour.\n\n**Body fields:** event_id (UUID), name, description, latitude, longitude, location, order_index, goal",
        tags=["Tour Stop"],
    ),
    update=extend_schema(
        summary="Cập nhật điểm dừng",
        tags=["Tour Stop"],
    ),
    partial_update=extend_schema(
        summary="Cập nhật một phần",
        tags=["Tour Stop"],
    ),
    destroy=extend_schema(
        summary="Xóa điểm dừng",
        tags=["Tour Stop"],
    ),
)
class TourStopViewSet(BaseViewSet, OAuthLibMixin):
    queryset = TourStop.objects.all()
    serializer_class = TourStopSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }
