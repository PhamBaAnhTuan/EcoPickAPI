from rest_framework import serializers
from .models import WasteReport, ReportImage


class WasteReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteReport
        fields = "__all__"


class ReportImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportImage
        fields = "__all__"
