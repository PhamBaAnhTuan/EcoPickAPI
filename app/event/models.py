from django.db import models
import uuid
from django.utils import timezone
from report.models import WasteReport
from user.models import User


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    organizer_id = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        related_name="events",
    )
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    cover_image_url = models.ImageField(
        upload_to="event_images/", blank=True, null=True
    )
    type = models.CharField(
        max_length=100, null=True, blank=True
    )  # cleanup, tree_planting, workshop, beach_cleanup, education, tour etc.
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(blank=True, null=True)
    max_paticipants = models.IntegerField(null=True, blank=True, default=50)
    current_paticipants = models.IntegerField(default=0)
    equipment = models.TextField(null=True, blank=True)
    difficulty = models.CharField(
        max_length=50, null=True, blank=True
    )  # easy, medium, hard
    eco_point_reward = models.IntegerField(default=100)
    status = models.CharField(
        max_length=50, default="upcoming"
    )  # upcoming, ongoing, completed, cancelled
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Event {self.id}"


class EventParticipants(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="participants",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events_joined",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50, default="joined"
    )  # joined, checked_in, completed, left, cancelled
    joined_at = models.DateTimeField(default=timezone.now)
    checked_in_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Participant {self.user} in Event {self.event}"

    class Meta:
        unique_together = ("event", "user")


class TourStop(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    event_id = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="tour_stops"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    order_index = models.IntegerField(default=0)
    goal = models.CharField(
        max_length=255, null=True, blank=True
    )  # e.g. "Pick up 10 pieces of trash", "Plant 5 trees", "Learn about local flora and fauna"
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Tour Stop {self.id}"