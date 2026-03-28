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
from drf_spectacular.utils import extend_schema, extend_schema_view
from app.swagger import badge_list_params, common_list_params


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách huy hiệu",
        description="Lấy tất cả huy hiệu. Hỗ trợ lọc badge_id, user_id.",
        parameters=badge_list_params,
        tags=["Badge"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết huy hiệu",
        description="Lấy chi tiết 1 huy hiệu bao gồm tên, mô tả, icon, category.",
        tags=["Badge"],
    ),
    create=extend_schema(
        summary="Tạo huy hiệu mới",
        description="Tạo huy hiệu mới.\n\n**Body fields:** name (unique, required), description, icon_url, category (reporting/events/social/streaks/exchange), equipment",
        tags=["Badge"],
    ),
    update=extend_schema(summary="Cập nhật huy hiệu", tags=["Badge"]),
    partial_update=extend_schema(summary="Cập nhật một phần huy hiệu", tags=["Badge"]),
    destroy=extend_schema(summary="Xóa huy hiệu", tags=["Badge"]),
)
class BadgeViewSet(BaseViewSet, OAuthLibMixin):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    filter_backends = [BadgeFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách huy hiệu user",
        description="Lấy tất cả huy hiệu đã trao cho users. Hỗ trợ lọc badge_id, user_id.",
        parameters=badge_list_params,
        tags=["User Badge"],
    ),
    retrieve=extend_schema(summary="Chi tiết huy hiệu user", tags=["User Badge"]),
    create=extend_schema(
        summary="Trao huy hiệu cho user",
        description="Trao huy hiệu cho user.\n\n**Body fields:** user_id (UUID FK), badge_id (UUID FK)\n\n**Unique constraint:** user_id + badge_id",
        tags=["User Badge"],
    ),
    update=extend_schema(summary="Cập nhật huy hiệu user", tags=["User Badge"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["User Badge"]),
    destroy=extend_schema(summary="Thu hồi huy hiệu", tags=["User Badge"]),
)
class UserBadgeViewSet(BaseViewSet, OAuthLibMixin):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer
    filter_backends = [BadgeFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách vật phẩm trao đổi",
        description="Lấy tất cả vật phẩm có thể trao đổi. Hỗ trợ lọc badge_id, user_id.",
        parameters=badge_list_params,
        tags=["Exchange Item"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết vật phẩm",
        description="Lấy chi tiết vật phẩm trao đổi.",
        tags=["Exchange Item"],
    ),
    create=extend_schema(
        summary="Đăng vật phẩm trao đổi",
        description="Đăng vật phẩm mới để trao đổi.\n\n**Body fields:** owner_id (UUID FK), name (unique, required), description, icon_url, category (tools/plants/seeds/reusable_items/educational_materials), condition (new/like_new/used/worn), type (physical/digital), exchange_for (eco_points/other_items/services), lastitude (float), longitude (float), location, address, status (available/pending/completed/cancelled)",
        tags=["Exchange Item"],
    ),
    update=extend_schema(summary="Cập nhật vật phẩm", tags=["Exchange Item"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Exchange Item"]),
    destroy=extend_schema(summary="Xóa vật phẩm", tags=["Exchange Item"]),
)
class ExchangeItemViewSet(BaseViewSet, OAuthLibMixin):
    queryset = ExchangItem.objects.all()
    serializer_class = ExchangeItemSerializer
    filter_backends = [BadgeFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }
