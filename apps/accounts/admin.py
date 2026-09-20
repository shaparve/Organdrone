from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
	list_filter = ('role', 'is_staff', 'is_active')
	search_fields = ('username', 'email')
	fieldsets = UserAdmin.fieldsets + (('OrganDrone access', {'fields': ('role',)}),)
	add_fieldsets = UserAdmin.add_fieldsets + (('OrganDrone access', {'fields': ('role',)}),)

# Register your models here.
