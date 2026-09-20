from django.contrib import admin

from .models import Delivery, Drone, DroneLocation


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
	list_display = ('identifier', 'operator', 'status', 'is_active')
	list_filter = ('status', 'is_active')
	search_fields = ('identifier', 'operator__username')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ('organ_request', 'drone', 'status', 'assigned_at', 'delivered_at')
	list_filter = ('status',)
	search_fields = ('drone__identifier',)


@admin.register(DroneLocation)
class DroneLocationAdmin(admin.ModelAdmin):
	list_display = ('drone', 'latitude', 'longitude', 'updated_at')
	search_fields = ('drone__identifier',)

# Register your models here.
