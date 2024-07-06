from account.models import User
from rest_framework import generics
from rest_framework import permissions
from account.serializers import UserSerializer
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProfileViewSet(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser]

    def get_object(self):
        return self.request.user