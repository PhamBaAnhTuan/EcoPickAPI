from rest_framework import serializers

from user.models import User
from .models import WasteReport, ReportImage


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class WasteReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(source="reporter_id", read_only=True)
    # reporter_id = serializers.UUIDField(source="reporter_id_id", read_only=True)

    class Meta:
        model = WasteReport
        # fields = "__all__"
        fields = [
            "id",
            "reporter",
            "reporter_id",
            "latitude",
            "longitude",
            "location",
            "address",
            "city",
            "country",
            "severity",
            "waste_type",
            "description",
            "status",
            "cleaned_by",
            "cleaned_at",
            "report_img",
            "created_at",
            "updated_at",
        ]


class ReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = "__all__"
