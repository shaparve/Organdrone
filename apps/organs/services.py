from django.db import transaction
from django.utils import timezone

from .models import Organ, OrganRequest


def find_matching_organs(organ_request):
    return Organ.objects.filter(
        organ_type=organ_request.organ_type,
        status=Organ.Status.AVAILABLE,
        expires_at__gt=timezone.now(),
    ).exclude(hospital=organ_request.requesting_hospital).select_related('hospital')


@transaction.atomic
def accept_request(organ_request, accepting_hospital, drone):
    request = OrganRequest.objects.select_for_update().get(pk=organ_request.pk)
    if request.status not in (OrganRequest.Status.OPEN, OrganRequest.Status.MATCHED):
        raise ValueError('This request has already been assigned or closed.')
    organ = request.matched_organ
    if not organ or organ.hospital_id != accepting_hospital.id:
        raise ValueError('The hospital does not own the matched organ.')
    organ = Organ.objects.select_for_update().get(pk=organ.pk)
    drone = drone.__class__.objects.select_for_update().get(pk=drone.pk)
    if organ.status != Organ.Status.AVAILABLE:
        raise ValueError('The matched organ is no longer available.')
    if drone.status != drone.Status.AVAILABLE or not drone.is_active:
        raise ValueError('The drone is not available.')
    from apps.logistics.models import Delivery
    if Delivery.objects.filter(organ_request=request).exists():
        raise ValueError('This request already has a delivery.')
    organ.status = Organ.Status.IN_TRANSIT
    organ.save(update_fields=['status'])
    drone.status = drone.Status.ASSIGNED
    drone.save(update_fields=['status'])
    request.accepted_by = accepting_hospital
    request.status = OrganRequest.Status.IN_DELIVERY
    request.save(update_fields=['accepted_by', 'status', 'updated_at'])
    return Delivery.objects.create(organ_request=request, organ=organ, drone=drone, status=Delivery.Status.ASSIGNED)
