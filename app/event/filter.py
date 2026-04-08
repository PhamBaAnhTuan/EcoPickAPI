from rest_framework.filters import BaseFilterBackend


class EventFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}

        event_id = request.query_params.get("event_id")
        user_id = request.query_params.get("user_id")
        if event_id:
            filters["event"] = event_id
        if user_id:
            filters["user"] = user_id

        queryset = queryset.filter(**filters)
        return queryset