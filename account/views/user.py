from account.models import User
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response
from account.serializers import UserSerializer
from rest_framework.filters import SearchFilter
from general.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields  = ['is_active', 'is_superuser', 'is_staff']
    search_fields = ['name']

    # allow unauthenticated user to create an account
    def get_permissions(self):
        if self.action == 'create':
            return []
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)