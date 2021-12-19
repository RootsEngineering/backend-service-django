from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersFilterSet(filters.FilterSet):
    strict = True

    class Meta:
        model = User
        fields = [
            'email',
            'is_active'
        ]
