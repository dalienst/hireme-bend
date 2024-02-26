from django.urls import path

from projects.views import (
    ProjectListCreateView,
    ProjectDetailView,
    BidDetailView,
    BidListCreateView,
    ProjectListView,
    ProjectsRetrieveView,
    AcceptBidsView,
    project_category_choices,
    project_status_choices,
    project_progress_choices,
    project_type_choices,
)

urlpatterns = [
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("projects/<str:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path("all-projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "all-projects/<str:slug>/",
        ProjectsRetrieveView.as_view(),
        name="projects-details",
    ),
    path("bids/", BidListCreateView.as_view(), name="bid-list-create"),
    path("bids/<str:slug>/", BidDetailView.as_view(), name="bid-detail"),
    path("bid/<str:slug>/", AcceptBidsView.as_view(), name="accept-bids"),
    path("category/", project_category_choices, name="project-category"),
    path("type/", project_type_choices, name="project-type"),
    path("status/", project_status_choices, name="project-status"),
    path("progress/", project_progress_choices, name="project-progress"),
]
