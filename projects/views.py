from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from projects.models import Project, Bid
from projects.serializers import ProjectSerializer, BidSerializer
from users.permissions import IsClient, IsDeveloper, IsDeveloperOrReadOnly


"""
Projects views
"""


class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [
        IsAuthenticated,
        IsClient,
    ]
    lookup_field = "slug"

    def delete(self, request: Request, *args, **kwargs) -> Response:
        """
        Returns message on deletion of projects
        """
        self.destroy(request, *args, **kwargs)
        return Response(
            {"message": "Project deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


"""
Bids views
"""


class BidListCreateView(generics.ListCreateAPIView):
    serializer_class = BidSerializer
    permission_classes = [
        IsAuthenticated,
        IsDeveloperOrReadOnly,
    ]

    def get_queryset(self):
        return Bid.objects.filter(developer=self.request.user)


class BidDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BidSerializer
    permission_classes = [
        IsAuthenticated,
        IsDeveloper,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Bid.objects.filter(developer=self.request.user)
