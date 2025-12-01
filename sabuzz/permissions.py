# sabuzz/permissions.py
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "admin"

class IsJournalist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "journalist"

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "user"

class IsAdminOrJournalist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ["admin", "journalist"]
