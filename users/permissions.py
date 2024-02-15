from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        return bool(obj == request.user)


class IsDeveloper(permissions.BasePermission):
    def has_permission(self, request, view: APIView):
        return bool(request.user.is_developer)

    def has_object_permission(self, request, view, obj):
        return bool(obj.developer == request.user)
