from django.conf import settings
from django.db import models


class Hospital(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hospital_profile')
	name = models.CharField(max_length=200, unique=True)
	address = models.TextField()
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)
	contact_phone = models.CharField(max_length=30)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

# Create your models here.
