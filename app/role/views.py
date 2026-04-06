from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Role
from .serializer import RoleSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from app.views.base import BaseViewSet


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách vai trò",
        description="Lấy tất cả vai trò (admin, organizer, moderator, user). Public endpoint - không cần xác thực.",
        tags=["Role"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết vai trò",
        description="Lấy chi tiết 1 vai trò theo ID.",
        tags=["Role"],
    ),
    create=extend_schema(
        summary="Tạo vai trò mới",
        description="Tạo vai trò mới.\n\n**Body fields:** id (string max 10, required), name (string max 200, unique, required), scope (text, optional)",
        tags=["Role"],
    ),
    update=extend_schema(summary="Cập nhật vai trò", tags=["Role"]),
    partial_update=extend_schema(summary="Cập nhật một phần vai trò", tags=["Role"]),
    destroy=extend_schema(summary="Xóa vai trò", tags=["Role"]),
)
class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [AllowAny]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"],["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"]],
        "create": [["admin"]],
        "destroy": [["admin"]],
    }
