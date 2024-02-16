from django.urls import path

from projects.views import (
    ProjectListCreateView,
    ProjectDetailView,
    BidDetailView,
    BidListCreateView,
    project_category_choices,
    project_availability_choices,
    project_progress_choices,
    project_type_choices,
)

urlpatterns = [
    path("projects/", ProjectListCreateView.as_view(), name="project-list-create"),
    path("projects/<str:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path("bids/", BidListCreateView.as_view(), name="bid-list-create"),
    path("bids/<str:slug>/", BidDetailView.as_view(), name="bid-detail"),
    path("category/", project_category_choices, name="project-category"),
    path("type/", project_type_choices, name="project-type"),
    path("availability/", project_availability_choices, name="project-availability"),
    path("progress/", project_progress_choices, name="project-progress"),
]
