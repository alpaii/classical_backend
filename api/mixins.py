from django.db.models import Count


class BaseFilterMixin:
    filter_fields = {}

    def apply_filters(self, queryset):
        """
        공통 필터링 로직을 적용하는 메서드
        """
        for param, field in self.filter_fields.items():
            value = self.request.query_params.get(param)
            if value:
                queryset = queryset.filter(**{field: value})

        return queryset
