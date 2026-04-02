from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet
from .models import WasteReport, ReportImage
from .serializer import WasteReportSerializer, ReportImageSerializer
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from app.swagger import common_list_params
from .filter import ReportFilter


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách báo cáo rác thải",
        description="Lấy tất cả báo cáo về rác thải / ô nhiễm.",
        parameters=common_list_params,
        tags=["Report"],
    ),
    retrieve=extend_schema(
        summary="Chi tiết báo cáo",
        description="Lấy chi tiết 1 báo cáo bao gồm vị trí, loại rác, mức độ nghiêm trọng, trạng thái.",
        tags=["Report"],
    ),
    create=extend_schema(
        summary="Tạo báo cáo mới",
        description="Tạo báo cáo rác thải mới. Scope: admin, user.\n\n**Body fields:** latitude (float, required), longitude (float, required), location, address, city, country, severity (string), waste_type, description, status (reported/verified/in_progress/cleaned), cleaned_by (UUID FK), cleaned_at",
        tags=["Report"],
    ),
    update=extend_schema(summary="Cập nhật báo cáo", tags=["Report"]),
    partial_update=extend_schema(summary="Cập nhật một phần báo cáo", tags=["Report"]),
    destroy=extend_schema(summary="Xóa báo cáo", tags=["Report"]),
)
class ReportViewSet(BaseViewSet, OAuthLibMixin):
    queryset = WasteReport.objects.select_related("reporter_id").all()
    serializer_class = WasteReportSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [ReportFilter]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }

    # def get_queryset(self):
    #     user = self.request.user

    #     if user.role and user.role.name == "admin":
    #         return WasteReport.objects.all()

    #     return WasteReport.objects.filter(reporter_id=user.id)


@extend_schema_view(
    list=extend_schema(
        summary="Danh sách hình ảnh báo cáo",
        description="Lấy tất cả hình ảnh đính kèm các báo cáo.",
        parameters=common_list_params,
        tags=["Report Image"],
    ),
    retrieve=extend_schema(summary="Chi tiết hình ảnh", tags=["Report Image"]),
    create=extend_schema(
        summary="Thêm hình ảnh báo cáo",
        description="Upload hình ảnh cho báo cáo.\n\n**Body fields:** report_id (UUID FK), url, thumbnail_url, height (int), width (int), order_index (int)",
        tags=["Report Image"],
    ),
    update=extend_schema(summary="Cập nhật hình ảnh", tags=["Report Image"]),
    partial_update=extend_schema(summary="Cập nhật một phần", tags=["Report Image"]),
    destroy=extend_schema(summary="Xóa hình ảnh", tags=["Report Image"]),
)
class ReportImageViewSet(BaseViewSet, OAuthLibMixin):
    queryset = ReportImage.objects.all()
    serializer_class = ReportImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "create": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "update": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "destroy": [["admin"]],
    }

    # def create(self, request, *args, **kwargs):
    #     print("\n=== DỮ LIỆU POST (REPORT) ===")
    #     import pprint

    #     pprint.pprint(dict(request.data))
    #     if request.FILES:
    #         print("--- FILES ---")
    #         pprint.pprint(dict(request.FILES))
    #     print("=============================\n")

    #     return super().create(request, *args, **kwargs)

    # def get_queryset(self):
    #     user = self.request.user

    #     if user.role and user.role.name == "admin":
    #         return ReportImage.objects.all()

    #     return ReportImage.objects.filter(user__id=user.id)
