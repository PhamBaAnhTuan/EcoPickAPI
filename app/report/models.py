from django.db import models
import uuid
from django.utils import timezone
from user.models import User


class WasteReport(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    severity = models.CharField(max_length=50, null=True, blank=True)
    waste_type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50, default="in_progress"
    )  # reported, verified, in_progress, cleaned
    upvote_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    cleaned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cleaned_reports",
    )
    cleaned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.location or f"Report {self.id}"


class ReportImage(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    report_id = models.ForeignKey(
        WasteReport, on_delete=models.CASCADE, related_name="images"
    )
    url = models.ImageField(upload_to="report_images/", blank=True, null=True)
    thumbnail_url = models.ImageField(
        upload_to="report_thumbnails/", blank=True, null=True
    )
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url or f"Image {self.id}"

    class Meta:
        db_table = "waste_report"
