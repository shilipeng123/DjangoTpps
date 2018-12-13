from rest_framework.permissions import BasePermission

from Admin.models import AdminUser


class SuperAdminUserPermissions(BasePermission):
    SAFE_METHODS = ["GET",'HEAD','OPTIONS']
    def has_permission(self, request, view):
        if request.method not in self.SAFE_METHODS:
            user = request.user

            return isinstance(user,AdminUser) and user.is_super
        return True
