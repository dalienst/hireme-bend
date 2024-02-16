from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project, Bid

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    """
    Projects serializers
    """

    name = serializers.CharField(min_length=1)
    description = serializers.CharField(min_length=1)
    project_category = serializers.CharField(
        min_length=2, source="get_project_category_display"
    )
    project_type = serializers.CharField(
        min_length=2, source="get_project_type_display"
    )
    project_duration = serializers.CharField(min_length=2)
    project_progress = serializers.CharField(
        min_length=1, source="get_project_progress_display"
    )
    project_status = serializers.CharField(
        min_length=1, source="get_project_status_display"
    )
    file = serializers.FileField(required=False, use_url=True)
    min_price = serializers.IntegerField()
    max_price = serializers.IntegerField()
    client = serializers.CharField(read_only=True, source="client.username")
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "description",
            "project_category",
            "project_type",
            "project_duration",
            "project_status",
            "project_progress",
            "file",
            "min_price",
            "max_price",
            "client",
            "slug",
        )

    def create(self, validated_data):
        validated_data["client"] = self.context["request"].user
        return Project.objects.create(**validated_data)


class BidSerializer(serializers.ModelSerializer):
    """
    Bid serializers
    """

    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(), slug_field="slug"
    )
    proposal = serializers.CharField(min_length=1)
    developer = serializers.CharField(read_only=True, source="developer.username")
    slug = serializers.SlugField(read_only=True)
    file = serializers.FileField(required=False, use_url=True)

    class Meta:
        model = Bid
        fields = (
            "id",
            "project",
            "proposal",
            "developer",
            "slug",
            "file",
        )

    def create(self, validated_data):
        validated_data["developer"] = self.context["request"].user
        return Bid.objects.create(**validated_data)
