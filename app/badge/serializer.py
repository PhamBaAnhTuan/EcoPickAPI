from rest_framework import serializers
from .models import Badge, UserBadge, ExchangItem


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"


class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = "__all__"


class ExchangeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangItem
        fields = "__all__"
