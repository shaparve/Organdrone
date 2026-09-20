from django.contrib import admin

from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
	list_display = ('name', 'contact_phone', 'is_active')
	list_filter = ('is_active',)
	search_fields = ('name', 'contact_phone')

# Register your models here.
