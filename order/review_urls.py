from django.urls import path,include
from order.views import ReviewViewSet
from rest_framework.routers import DefaultRouter

review_router = DefaultRouter()
review_router.register('', ReviewViewSet)

urlpatterns = [
    path('', include(review_router.urls)),
    path('<int:pk>/visibility/', ReviewViewSet.as_view({'post':'set_visibility'}), name='review-set-visibility'),
]