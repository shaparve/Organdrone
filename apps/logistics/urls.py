from rest_framework.routers import DefaultRouter

from .views import DroneLocationViewSet, DroneViewSet

router = DefaultRouter()
router.register('drones', DroneViewSet, basename='drone')
router.register('drone-locations', DroneLocationViewSet, basename='drone-location')
urlpatterns = router.urls
