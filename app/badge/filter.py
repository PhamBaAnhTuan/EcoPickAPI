from rest_framework.filters import BaseFilterBackend


class BadgeFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}

        badge_id = request.query_params.get("badge_id")
        user_id = request.query_params.get("user_id")
        if badge_id:
            filters["badge_id"] = badge_id
        if user_id:
            filters["user_id"] = user_id

        queryset = queryset.filter(**filters)
        return queryset
