from rest_framework import serializers
from .models import Badge, UserBadge, ExchangItem


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"


class BadgeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = [
            "id",
            "name",
            "icon_url",
        ]


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeShortSerializer(source="badge_id", read_only=True)

    class Meta:
        model = UserBadge
        fields = [
            "id",
            "user_id",
            "badge_id",
            "badge",
            "awarded_at",
        ]


class ExchangeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangItem
        fields = "__all__"
