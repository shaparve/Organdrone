from django.conf import settings
from django.db import models


class Drone(models.Model):
	class Status(models.TextChoices):
		AVAILABLE = 'AVAILABLE', 'Available'
		ASSIGNED = 'ASSIGNED', 'Assigned'
		IN_FLIGHT = 'IN_FLIGHT', 'In flight'
		MAINTENANCE = 'MAINTENANCE', 'Maintenance'

	operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='drones')
	identifier = models.CharField(max_length=50, unique=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
	is_active = models.BooleanField(default=True)


class Delivery(models.Model):
	class Status(models.TextChoices):
		ASSIGNED = 'ASSIGNED', 'Assigned'
		IN_TRANSIT = 'IN_TRANSIT', 'In transit'
		DELIVERED = 'DELIVERED', 'Delivered'
		CANCELLED = 'CANCELLED', 'Cancelled'

	organ_request = models.OneToOneField('organs.OrganRequest', on_delete=models.PROTECT, related_name='delivery')
	organ = models.OneToOneField('organs.Organ', on_delete=models.PROTECT, related_name='delivery')
	drone = models.OneToOneField(Drone, on_delete=models.PROTECT, related_name='delivery')
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED)
	assigned_at = models.DateTimeField(auto_now_add=True)
	delivered_at = models.DateTimeField(null=True, blank=True)


class DroneLocation(models.Model):
	drone = models.OneToOneField(Drone, on_delete=models.CASCADE, related_name='location')
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
