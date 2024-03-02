from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import DeveloperProfile
from users.serializers import (
    UserSerializer,
    DeveloperProfileSerializer,
    DeveloperSerializer,
    LogoutSerializer,
)
from users.permissions import IsUser, IsDeveloper

User = get_user_model()


"""
Users/Clients
-create account
-update account details
-delete account
"""


class UserRegister(APIView):
    """
    Handle POST requests to create a new user.

    Args:
        request (Request): The request object.
        format (str, optional): The format of the response. Defaults to "json".

    Returns:
        Response: The HTTP response with the created user data.
    """

    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = "id"
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ClientDeveloperProfileView(generics.RetrieveAPIView):
    serializer_class = DeveloperProfileSerializer
    queryset = DeveloperProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.kwargs.get("username")
        return self.get_queryset().get(developer__username=username)


"""
Developer Views
-create developer account
-update developer details
-delete developer
"""


class DeveloperRegister(APIView):

    def post(self, request: Request, format: str = "json") -> Response:
        serializer = DeveloperSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class DeveloperListView(generics.ListAPIView):
    serializer_class = DeveloperSerializer
    queryset = User.objects.filter(is_developer=True)
    permission_classes = (IsAuthenticated,)


class DeveloperProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeveloperProfileSerializer
    lookup_field = "developer"
    queryset = DeveloperProfile.objects.all()
    permission_classes = [IsAuthenticated, IsDeveloper]


class DeveloperProfileListView(generics.ListAPIView):
    serializer_class = DeveloperProfileSerializer
    queryset = DeveloperProfile.objects.all()
    permission_classes = (IsAuthenticated,)


"""
Logout
"""


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):  # type:ignore[no-untyped-def]
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
