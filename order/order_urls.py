from order.views import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderViewSet)

urlpatterns = router.urls