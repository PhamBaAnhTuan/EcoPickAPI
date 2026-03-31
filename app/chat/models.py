from django.db import models
import uuid
from django.utils import timezone
from event.models import Event
from user.models import User

class Conversation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    type = models.CharField(max_length=50, null=True, blank=True)  # one_on_one, group
    event_id = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="conversations")
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or f"Conversation {self.id}"
    
    
class ConversationMember(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='members')
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='conversations')
    joined_at = models.DateTimeField(default=timezone.now)
    last_read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Member {self.user_id} in Conversation {self.conversation_id}"
    
class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_messages')
    content = models.TextField(null=True, blank=True)
    photo_url = models.ImageField(upload_to="message_images/", blank=True, null=True)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message {self.id} in Conversation {self.conversation_id}"
    
class PointLog(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='point_logs')
    points = models.IntegerField()
    reason = models.CharField(max_length=255, null=True, blank=True)       #report_created, event_completed, reward_redeemed...
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"PointLog {self.id} for User {self.user_id}"