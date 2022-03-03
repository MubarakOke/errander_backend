from rest_framework import permissions

class SuperuserPermissionOnly(permissions.BasePermission):
    """
    Superuser permission only
    """
    def has_permission(self, request, view):
        try:
            return request.user.is_super_admin
        except AttributeError:
            return False


class CreatePermissionOnly(permissions.BasePermission):
    """
    Post request permission only
    """
    def has_permission(self, request, view):
        return request.method == 'POST'


# class IndividualAdminPermission(permissions.BasePermission):
#     """
#     Object owner permission only
#     """
#     def has_object_permission(self, request, view, obj):
#         return obj.admin.user == request.user or request.user.is_super_admin