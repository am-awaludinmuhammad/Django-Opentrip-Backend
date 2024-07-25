from order.models import Review
from django.http import Http404
from account.utils import user_is_admin
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from general.pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from order.serializers import ReviewSerializer, SetReviewVisibilitySerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    
    queryset = Review.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    search_fields = ['order__trip__name']
    filterset_fields = ['created_at', 'rate', 'is_visible']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user_is_admin(user):
            return queryset.all()
        else:
            return queryset.filter(order__user=user)
    
    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset()

        try:
            if user_is_admin(user):
                return queryset.get(pk=pk)
            else:
                return queryset.get(pk=pk, order__user=user)
        except  queryset.model.DoesNotExist:
            raise Http404("Object not found.")
        
    @extend_schema(request=SetReviewVisibilitySerializer, responses=SetReviewVisibilitySerializer)
    def set_visibility(self, request, *args, **kwargs):
        if not user_is_admin(request.user):
            return Response({'detail': 'Forbidden'}, status.HTTP_403_FORBIDDEN)

        review = self.get_object()
        serializer = SetReviewVisibilitySerializer(review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)