from trip.views import TripViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', TripViewSet)

urlpatterns = router.urls