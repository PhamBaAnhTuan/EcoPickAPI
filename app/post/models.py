from django.db import models
import uuid
from django.utils import timezone
from user.models import User
from report.models import WasteReport
from event.models import Event


class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    author_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    hashtags = models.CharField(
        max_length=255, null=True, blank=True
    )  # comma-separated hashtags
    tagged_users = models.JSONField(
        default=list,
        blank=True,
        help_text="Danh sách UUID dạng string, VD: ['uuid-1', 'uuid-2']",
    )
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    related_report_id = models.ForeignKey(
        WasteReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    related_event_id = models.ForeignKey(
        Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts"
    )
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Post {self.id}"


class PostMedia(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="media")
    url = models.ImageField(upload_to="post_images/", blank=True, null=True)
    thumbnail_url = models.ImageField(upload_to="post_thumbnails/", blank=True, null=True)
    type = models.CharField(max_length=50, null=True, blank=True)  # image, video, etc.
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    order_index = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url or f"Media {self.id}"


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments"
    )
    repost_id = models.ForeignKey(
        WasteReport,
        on_delete=models.CASCADE,
        related_name="reposts",
        null=True,
        blank=True,
    )
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    event_id = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    content = models.TextField(null=True, blank=True)
    photo_url = models.ImageField(
        upload_to="comment_images/", blank=True, null=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user_id} on Post {self.post_id}"


class Like(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="likes"
    )
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    repost_id = models.ForeignKey(
        WasteReport,
        on_delete=models.CASCADE,
        related_name="like_reposts",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Like by {self.user_id} on Post {self.post_id}"

    class Meta:
        unique_together = ["user_id", "post_id", "repost_id"]
