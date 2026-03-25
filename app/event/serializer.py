from rest_framework import serializers
from .models import Event, EventParticipants, TourStop


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
class EventParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventParticipants
        fields = "__all__"
class TourStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourStop
        fields = "__all__"