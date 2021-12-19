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

    @action(detail=True, methods=['get'])
    def reports(self, request, pk):
        user = self.get_object()
        users = user.reports.all()
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


    def reports(first_user_numbers: User.pk):
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
    
    def get_queryset(self):
        company = self.request.user.company
        return User.objects.filter(company=company)
