from django.urls import path

from projects.views import (
    ProjectListCreateView,
    ProjectDetailView,
    BidDetailView,
    BidListCreateView

)

urlpatterns = [
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path("bids/", BidListCreateView.as_view(), name="bid-list-create"),
    path("bids/<slug:slug>/", BidDetailView.as_view(), name="bid-detail"),
]