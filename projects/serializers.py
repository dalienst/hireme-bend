from django.contrib.auth import get_user_model
from rest_framework import serializers

from projects.models import Project, Bid
from users.serializers import DeveloperSerializer

User = get_user_model()


class BidSerializer(serializers.ModelSerializer):
    """
    Bid serializers
    """

    project = serializers.SlugRelatedField(
        queryset=Project.objects.all(), slug_field="slug"
    )
    proposal = serializers.CharField(min_length=1)
    developer = DeveloperSerializer(read_only=True)
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
            "status",
        )

    def create(self, validated_data):
        validated_data["developer"] = self.context["request"].user
        return Bid.objects.create(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    """
    Projects serializers
    """

    name = serializers.CharField(min_length=1)
    description = serializers.CharField(min_length=1)
    project_category = serializers.CharField(min_length=2)
    project_type = serializers.CharField(min_length=2)
    project_duration = serializers.CharField(min_length=2)
    project_progress = serializers.CharField(min_length=1)
    project_status = serializers.CharField(min_length=1)
    file = serializers.FileField(required=False, use_url=True)
    min_price = serializers.IntegerField()
    max_price = serializers.IntegerField()
    client = serializers.CharField(read_only=True, source="client.username")
    slug = serializers.SlugField(read_only=True)
    bids = serializers.SerializerMethodField(read_only=True)

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
            "bids",
        )

    def create(self, validated_data):
        validated_data["client"] = self.context["request"].user
        return Project.objects.create(**validated_data)

    def get_bids(self, obj):
        bids = Bid.objects.filter(project=obj)
        serializer = BidSerializer(bids, many=True)
        return serializer.data
