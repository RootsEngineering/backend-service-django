from django_filters import rest_framework as filters, BooleanFilter
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersFilterSet(filters.FilterSet):
    strict = True
    with_reports = BooleanFilter(field_name='reports_to', method='filter_with_reports')

    class Meta:
        model = User
        fields = [
            'email',
            'is_active'
        ]

    def filter_with_reports(self, queryset, name, value):
        if value:
            queryset = queryset.filter(reports_to_id__isnull=False)
            return queryset
        queryset = queryset.filter(reports_to_id__isnull=True)
        return queryset
