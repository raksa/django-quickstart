from rest_framework.permissions import BasePermission


class SuperAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not (user and user.is_authenticated):
            return False

        if user.is_superuser:
            return True

        return False
