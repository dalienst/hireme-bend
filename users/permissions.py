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


class IsClient(permissions.BasePermission):
    def has_permission(self, request, view: APIView):
        return bool(request.user.is_client)

    def has_object_permission(self, request, view, obj):
        return bool(obj.client == request.user)


class IsDeveloperOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to developers.
        return request.user and request.user.is_authenticated and request.user.is_developer

