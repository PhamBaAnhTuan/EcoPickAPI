from oauth2_provider.views.mixins import OAuthLibMixin
from app.views.base import BaseViewSet

from app.views.base import BaseViewSet
from .models import WasteReport, ReportImage
from .serializer import WasteReportSerializer, ReportImageSerializer
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


class ReportViewSet(BaseViewSet, OAuthLibMixin):
    queryset = WasteReport.objects.all()
    serializer_class = WasteReportSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"], ["user"]],
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
    #         return WasteReport.objects.all()
    #     return WasteReport.objects.filter(user_id=user.id)


class ReportImageViewSet(BaseViewSet, OAuthLibMixin):
    queryset = ReportImage.objects.all()
    serializer_class = ReportImageSerializer
    required_alternate_scopes = {
        "list": [["admin"], ["organizer"], ["moderator"], ["user"]],
        "retrieve": [["admin"], ["organizer"], ["moderator"]],
        "create": [["admin"], ["user"]],
        "update": [["admin"]],
        "destroy": [["admin"]],
    }
