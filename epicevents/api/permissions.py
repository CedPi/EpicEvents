from rest_framework import permissions


SAFE_METHODS = ['GET']
EVENT_PERMS = ['GET', 'PUT']


class IsSales(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Sales') or request.method in SAFE_METHODS:
            return True
        return False


class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Support'):
            return True
        return False


class IsClientOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.sales_contact == request.user or request.method in SAFE_METHODS:
            return True
        return False


class IsContractOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.sales_contact == request.user or request.method in SAFE_METHODS:
            return True
        return False


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.created_by == request.user or request.method in SAFE_METHODS:
            return True
        return False


class HasEventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in EVENT_PERMS

    def has_object_permission(self, request, view, obj):
        return obj.support_contact == request.user
