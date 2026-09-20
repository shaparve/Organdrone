from rest_framework import viewsets

from apps.accounts.permissions import IsDroneOperator
from .models import Drone, DroneLocation
from .serializers import DroneLocationSerializer, DroneSerializer


class DroneViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = DroneSerializer
	permission_classes = (IsDroneOperator,)

	def get_queryset(self):
		return Drone.objects.filter(operator=self.request.user).select_related('location', 'delivery')


class DroneLocationViewSet(viewsets.ModelViewSet):
	serializer_class = DroneLocationSerializer
	permission_classes = (IsDroneOperator,)
	http_method_names = ('get', 'put', 'patch', 'head', 'options')

	def get_queryset(self):
		return DroneLocation.objects.filter(drone__operator=self.request.user).select_related('drone', 'drone__delivery')

# Create your views here.
