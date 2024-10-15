from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer

class IsAdminUser(permissions.BasePermission):
    """
    Permission class to check if the user is an admin
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff