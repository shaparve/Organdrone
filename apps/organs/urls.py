from rest_framework.routers import DefaultRouter

from .views import OrganRequestViewSet

router = DefaultRouter()
router.register('organ-requests', OrganRequestViewSet, basename='organ-request')
urlpatterns = router.urls
