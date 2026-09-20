from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role in self.allowed_roles
        )


class IsHospital(HasRole):
    allowed_roles = ('HOSPITAL',)


class IsDroneOperator(HasRole):
    allowed_roles = ('DRONE_OPERATOR',)


class IsAdmin(HasRole):
    allowed_roles = ('ADMIN',)
