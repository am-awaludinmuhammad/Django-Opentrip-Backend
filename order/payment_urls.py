from django.urls import path
from order.views import PaymentViewSet

urlpatterns = [
    path('', PaymentViewSet.as_view({'post': 'create'}), name='payment'),
    path('<int:pk>/confirm/', PaymentViewSet.as_view({'post':'confirm'}), name='payment-confirm'),
]