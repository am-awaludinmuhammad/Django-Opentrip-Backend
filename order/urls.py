from django.urls import path,include
from order.views import OrderViewSet, PaymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderViewSet)

urlpatterns = [
    path('payments/', PaymentViewSet.as_view({'post': 'create'}), name='payment'),
    path('payments/<int:pk>/confirm/', PaymentViewSet.as_view({'post':'confirm'}), name='payment-confirm'),
]
urlpatterns += router.urls