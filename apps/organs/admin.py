from django.contrib import admin

from .models import Organ, OrganRequest


@admin.register(Organ)
class OrganAdmin(admin.ModelAdmin):
	list_display = ('organ_type', 'hospital', 'status', 'expires_at')
	list_filter = ('organ_type', 'status')
	search_fields = ('donor_reference', 'hospital__name')


@admin.register(OrganRequest)
class OrganRequestAdmin(admin.ModelAdmin):
	list_display = ('organ_type', 'requesting_hospital', 'priority', 'status', 'required_by')
	list_filter = ('organ_type', 'priority', 'status')
	search_fields = ('requesting_hospital__name',)

# Register your models here.
