from django.db import models
import uuid
from django.utils import timezone
from user.models import User


class Badge(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    # icon_url = models.ImageField(upload_to="badge_icons/", blank=True, null=True)
    icon_url = models.CharField(max_length=255, null=True, blank=True)
    category = models.TextField(
        null=True, blank=True
    )  # reporting, events, social, streaks, exchange
    equipment = models.TextField(null=True, blank=True)  # for event badges
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Badge {self.id}"


class UserBadge(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge_id = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")
    awarded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Badge {self.badge_id} awarded to User {self.user_id}"

    class Meta:
        unique_together = ["user_id", "badge_id"]


class ExchangItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    owner_id = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exchange_items",
    )
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    # icon_url = models.ImageField(upload_to="exchange_items_images/", blank=True, null=True)
    icon_url = models.CharField(max_length=255, null=True, blank=True)
    category = models.TextField(
        null=True, blank=True
    )  # tools, plants, seeds, reusable_items, educational_materials etc.
    condition = models.CharField(
        max_length=50, null=True, blank=True
    )  # new, like_new, used, worn
    type = models.CharField(max_length=50, null=True, blank=True)  # physical, digital
    exchange_for = models.TextField(
        null=True, blank=True
    )  # eco_points, other_items, services
    lastitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50, default="available"
    )  # available, pending, completed, cancelled
    request_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Exchange Item {self.id}"
