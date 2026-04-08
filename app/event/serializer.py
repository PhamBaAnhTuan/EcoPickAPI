from rest_framework import serializers
from .models import Event, EventParticipants, TourStop
from user.serializers import UserInfoShortSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class EventParticipantsSerializer(serializers.ModelSerializer):
    participant = UserInfoShortSerializer(source="user", read_only=True)
    class Meta:
        model = EventParticipants
        fields = [
            "id",
            "event",
            "user",
            "checked_in_at",
            "joined_at",
            "status",
            "participant"
        ]
        # fields = "__all__"
        
class TourStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourStop
        fields = "__all__"