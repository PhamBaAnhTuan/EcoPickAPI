from rest_framework import serializers
from .models import Conversation, ConversationMember, Message, PointLog


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = "__all__"

class ConversationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMember
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class PointLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointLog
        fields = "__all__"
