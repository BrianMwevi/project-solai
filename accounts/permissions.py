from rest_framework import permissions


class CanGenerate(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.api_key is None


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return perform_check(request, "ADMIN")


class IsInvestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, "INVESTOR")


class IsTrader(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, "TRADER")


class IsDeveloper(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, "DEVELOPER")


def perform_check(request, role):
    return request.user.role == role
