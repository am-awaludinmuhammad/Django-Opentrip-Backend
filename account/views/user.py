from account.models import User
from rest_framework import viewsets, status
from django.utils.encoding import force_str
from rest_framework.response import Response
from rest_framework import permissions, views
from account.serializers import UserSerializer
from rest_framework.filters import SearchFilter
from account.utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from account.tokens import account_activation_token
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

    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email(user)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class VerifyEmailView(views.APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user,token):
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Email berhasil diverifikasi.'})
        else:
            return Response({'error': 'Link verifikasi tidak valid!'}, status=status.HTTP_400_BAD_REQUEST)
