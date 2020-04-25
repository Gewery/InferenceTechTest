from rest_framework import permissions


class IsSender(permissions.BasePermission):
    """
    Check whether current user is a sender of an object(message)
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender


class IsRecipient(permissions.BasePermission):
    """
    Check whether current user is a recipient of an object(message)
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.recipient


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Check whether current user is a sender of an object(message) or the method is safe (GET, HEAD, OPTIONS)
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.sender
