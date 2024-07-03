from rest_framework import viewsets, status
from rest_framework.response import Response
from account.models import User
from account.serializers import UserSerializer
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # allow unauthenticated user to create an account
    def get_permissions(self):
        if self.action == 'create':
            return []
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)