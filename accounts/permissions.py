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

class UpdatePermissionOnly(permissions.BasePermission):
    """
    Put request permission only
    """
    def has_permission(self, request, view):
        print(request.method)
        return request.method == 'PATCH' or request.method == 'PUT'


class OrderCreatorOrUpdatePermission(permissions.BasePermission):
    """
    Object owner permission only
    """
    def has_object_permission(self, request, view, obj):
        try:
            return request.user.is_admin or obj.customer.user == request.user or obj.errander.user==request.user or request.method=="PUT" or request.method=="PATCH"
        except:
            return request.user.is_admin or obj.customer.user == request.user or request.method=="PUT" or request.method=="PATCH"