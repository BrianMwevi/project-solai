from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework_api_key.models import APIKey

User = get_user_model()


class CanGenerateKey(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.api_key is None


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return perform_check(request, "ADMIN")


class IsStockAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        user = User.objects.filter(api_key=api_key).first()
        # TODO: Verify request is from the same domain
        # current_site = get_current_site(request)
        # origin = request.META['REMOTE_ADDR']
        # print("Domain: ", current_site.name)
        # print("Origin: ", origin)
        return user is not None and user.role == 'ADMIN'


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
