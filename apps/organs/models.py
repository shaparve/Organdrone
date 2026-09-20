from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Organ(models.Model):
	class OrganType(models.TextChoices):
		HEART = 'HEART', 'Heart'
		LIVER = 'LIVER', 'Liver'
		KIDNEY = 'KIDNEY', 'Kidney'
		LUNG = 'LUNG', 'Lung'
		PANCREAS = 'PANCREAS', 'Pancreas'
		CORNEA = 'CORNEA', 'Cornea'

	class Status(models.TextChoices):
		AVAILABLE = 'AVAILABLE', 'Available'
		RESERVED = 'RESERVED', 'Reserved'
		IN_TRANSIT = 'IN_TRANSIT', 'In transit'
		DELIVERED = 'DELIVERED', 'Delivered'
		EXPIRED = 'EXPIRED', 'Expired'

	hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.PROTECT, related_name='organs')
	organ_type = models.CharField(max_length=20, choices=OrganType.choices)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
	donor_reference = models.CharField(max_length=100, unique=True)
	available_at = models.DateTimeField(default=timezone.now)
	expires_at = models.DateTimeField()

	class Meta:
		constraints = [models.CheckConstraint(check=models.Q(expires_at__gt=models.F('available_at')), name='organ_expiry_after_available')]


class OrganRequest(models.Model):
	class Priority(models.TextChoices):
		LOW = 'LOW', 'Low'
		MEDIUM = 'MEDIUM', 'Medium'
		HIGH = 'HIGH', 'High'
		CRITICAL = 'CRITICAL', 'Critical'

	class Status(models.TextChoices):
		OPEN = 'OPEN', 'Open'
		MATCHED = 'MATCHED', 'Matched'
		ACCEPTED = 'ACCEPTED', 'Accepted'
		IN_DELIVERY = 'IN_DELIVERY', 'In delivery'
		COMPLETED = 'COMPLETED', 'Completed'
		CANCELLED = 'CANCELLED', 'Cancelled'

	requesting_hospital = models.ForeignKey('hospitals.Hospital', on_delete=models.PROTECT, related_name='organ_requests')
	organ_type = models.CharField(max_length=20, choices=Organ.OrganType.choices)
	priority = models.CharField(max_length=10, choices=Priority.choices)
	required_by = models.DateTimeField(validators=[MinValueValidator(timezone.now)])
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
	matched_organ = models.ForeignKey(Organ, null=True, blank=True, on_delete=models.PROTECT, related_name='matched_requests')
	accepted_by = models.ForeignKey('hospitals.Hospital', null=True, blank=True, on_delete=models.PROTECT, related_name='accepted_requests')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		constraints = [models.CheckConstraint(check=~models.Q(requesting_hospital=models.F('accepted_by')), name='requesting_and_accepting_hospital_differ')]

# Create your models here.
