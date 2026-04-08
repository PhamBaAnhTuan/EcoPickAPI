from django.db import models
import uuid
from django.utils import timezone

class RoleName(models.TextChoices):
    ADMIN = "admin", "admin:full_access"
    ORGANIZER = "organizer", "organizer:basic_access"
    MODERATOR = "moderator", "moderator:basic_access"
    USER = "user", "user:basic_access"

class Role(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(
        max_length=200, null=False, blank=False, unique=True, choices=RoleName.choices, default=RoleName.USER
    )
    scope = models.TextField(default="", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_scope(self):
        return self.scope.strip().split()

    class Meta:
        db_table = "role"
