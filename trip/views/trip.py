from trip.models import Trip
from rest_framework import viewsets
from trip.filtersets.trip import TripFilter
from rest_framework.exceptions import NotFound
from rest_framework import permissions, filters
from trip.serializers.trip import TripSerializer
from rest_framework.exceptions import MethodNotAllowed
from drf_nested_forms.parsers import NestedMultiPartParser
from django_filters.rest_framework import DjangoFilterBackend

class TripViewSet(viewsets.ModelViewSet):
    parser_classes = [NestedMultiPartParser]
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_class = TripFilter
    search_fields = ['name','regency__name','regency__province__name']

    # optional get trip object by pk or by slug
    def get_object(self):
        lookup_value = self.kwargs.get('pk')
        try:
            return Trip.objects.get(pk=int(lookup_value))
        except (Trip.DoesNotExist, ValueError):
            pass

        try:
            return Trip.objects.get(slug=lookup_value)
        except Trip.DoesNotExist:
            raise NotFound(detail="No Trip matches the given query.", code=404)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')