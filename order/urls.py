from django.urls import path
from order.views import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderViewSet)

# urlpatterns = [
#     path('', OrderViewSet.as_view(), name='order'),
# ]

urlpatterns = router.urls