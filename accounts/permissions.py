from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return perform_check(request, "ADMIN")


class IsInvestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, "IVESTOR")


class IsTrader(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, "TRADER")


class IsDeveloper(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, "DEVELOPER")


def perform_check(request, role):
    if not request.user.is_authenticated:
        return False
    return request.user.role == role
