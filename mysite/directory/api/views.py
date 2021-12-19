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

    def get_queryset(self):
        return User.objects.all()
