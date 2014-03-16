from rest_framework import permissions


class IsStaffOrTargetUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user


class IsOwner(permissions.BasePermission):
    """a user can edit only their own posts"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
