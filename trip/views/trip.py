from rest_framework import viewsets
from trip.models import Trip
from trip.serializers.trip import TripSerializer
from rest_framework import permissions
from drf_nested_forms.parsers import NestedMultiPartParser
from rest_framework.exceptions import MethodNotAllowed

class TripViewSet(viewsets.ModelViewSet):
    parser_classes = [NestedMultiPartParser]
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')