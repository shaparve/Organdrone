from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsHospital
from apps.hospitals.models import Hospital
from .models import OrganRequest
from .serializers import MatchSerializer, OrganRequestSerializer
from .services import accept_request, find_matching_organs


class OrganRequestViewSet(viewsets.ModelViewSet):
	serializer_class = OrganRequestSerializer
	permission_classes = (IsHospital,)

	def get_queryset(self):
		return OrganRequest.objects.select_related('requesting_hospital', 'matched_organ', 'accepted_by').filter(requesting_hospital__user=self.request.user)

	def perform_create(self, serializer):
		organ_request = serializer.save(requesting_hospital=Hospital.objects.get(user=self.request.user))
		matched_organ = find_matching_organs(organ_request).first()
		if matched_organ:
			organ_request.matched_organ = matched_organ
			organ_request.status = OrganRequest.Status.MATCHED
			organ_request.save(update_fields=('matched_organ', 'status', 'updated_at'))

	@action(detail=True, methods=('get',), url_path='matches')
	def matches(self, request, pk=None):
		return Response(MatchSerializer(find_matching_organs(self.get_object()), many=True).data)

	@action(detail=True, methods=('post',), url_path='accept')
	def accept(self, request, pk=None):
		organ_request = OrganRequest.objects.get(pk=pk)
		hospital = Hospital.objects.get(user=request.user)
		from apps.logistics.models import Drone
		drone = Drone.objects.filter(pk=request.data.get('drone'), is_active=True).first()
		if not drone:
			return Response({'detail': 'A valid operator drone is required.'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			delivery = accept_request(organ_request, hospital, drone)
		except ValueError as exc:
			return Response({'detail': str(exc)}, status=status.HTTP_409_CONFLICT)
		return Response({'delivery_id': delivery.id, 'status': delivery.status}, status=status.HTTP_201_CREATED)

# Create your views here.
