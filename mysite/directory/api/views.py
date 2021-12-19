from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from directory.api.filtersets import UsersFilterSet
from directory.api.serializers import UserSerializer
from directory.models import User


class UsersViewSet(viewsets.ModelViewSet):
    """
    Endpoint for returning User data.
    """

    filterset_class = UsersFilterSet
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def reports(self, request, pk):
        user = self.get_object()
        users = User.objects.filter(pk__in=[u for u in find_reports(user.pk)])
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def managers(self, request, pk):
        user = self.get_object()
        users = User.objects.filter(pk__in=[u for u in find_managers(user.reports_to_id)])
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        company = self.request.user.company
        return User.objects.filter(company=company)


def find_reports(first_user_numbers: User.pk):
    reports_id_list = []
    while first_user_numbers:
        if type(first_user_numbers) != int:
            users = User.objects.filter(reports_to_id__in=[num for num in first_user_numbers])
            first_user_numbers = [u.pk for u in users]
            reports_id_list.extend(first_user_numbers)
        else:
            users = User.objects.filter(reports_to_id__exact=first_user_numbers)
            first_user_numbers = [u.pk for u in users]
            reports_id_list.extend(first_user_numbers)
    return reports_id_list


def find_managers(reports_to_num: User.reports_to):
    managers_id_list = [reports_to_num]
    while reports_to_num is not None:
        users = User.objects.filter(pk__exact=reports_to_num)
        reports_to_num = users[0].reports_to_id
        managers_id_list.append(reports_to_num)
    return managers_id_list