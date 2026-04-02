from rest_framework.filters import BaseFilterBackend


class ReportFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {}

        reporter_id = request.query_params.get("reporter_id")
        if reporter_id:
            filters["reporter_id"] = reporter_id

        queryset = queryset.filter(**filters)
        return queryset
