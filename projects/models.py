from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from users.abstracts import TimeStampedModel, UniversalIdModel

User = get_user_model()


class Project(UniversalIdModel, TimeStampedModel):
    """
    clients create projects
    """

    name = models.CharField(max_length=1000)
    PROJECT_TYPE = (
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Contract", "Contract"),
    )
    project_type = models.CharField(
        max_length=200, choices=PROJECT_TYPE, default="Full Time"
    )
    PROJECT_CATEGORY = (
        ("Web Development", "Web Development"),
        ("Database", "Database"),
        ("Machine Learning", "Machine Learning"),
        ("Artificial Intelligence", "Artificial Intelligence"),
        ("Data Science", "Data Science"),
    )
    project_category = models.CharField(
        max_length=255, choices=PROJECT_CATEGORY, default="Web Development"
    )
    PROJECT_PROGRESS = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed"),
    )
    project_progress = models.CharField(
        max_length=100, choices=PROJECT_PROGRESS, default="Pending"
    )
    PROJECT_STATUS = (
        ("Available", "Available"),
        ("Not Available", "Not Available"),
    )
    project_status = models.CharField(
        max_length=100, choices=PROJECT_STATUS, default="Available"
    )
    description = models.TextField()
    project_duration = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    file = CloudinaryField("file", null=True, blank=True)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    @property
    def price_range(self):
        if self.min_price is not None and self.max_price is not None:
            return f"{self.min_price} - {self.max_price}"
        return None

    @price_range.setter
    def price_range(self, value):
        parts = value.split(" - ")
        if len(parts) == 2:
            self.min_price = Decimal(parts[0])
            self.max_price = Decimal(parts[1])
        else:
            raise ValueError("Invalid price range format. Use 'min - max'.")

    def __str__(self) -> str:
        return self.name


@receiver(pre_save, sender=Project)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(f"{instance.id}-{instance.name}")


class Bid(UniversalIdModel, TimeStampedModel):
    """
    The model for developers to place bids on projects posted by clients
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bids")
    proposal = models.TextField()
    developer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    file = CloudinaryField("proposal", null=True, blank=True)

    BID_STATUS = (
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    )

    status = models.CharField(max_length=100, choices=BID_STATUS, default="Pending")
    slug = models.SlugField(max_length=400, unique=True, blank=True, null=True)

    class Meta:
        ordering = ["project"]

    def clean(self):
        super().clean()

        # Ensure that the developer is not bidding on their own project
        if self.developer == self.project.client:
            raise ValidationError("You cannot bid on your own project.")

        # Ensure that the developer has not already placed a bid on this project
        existing_bids = Bid.objects.filter(
            project=self.project, developer=self.developer
        )
        if existing_bids.exists():
            raise ValidationError("You have already placed a bid on this project.")

    def __str__(self) -> str:
        return self.project.name


@receiver(pre_save, sender=Bid)
def slug_pre_save(sender, instance, **kwargs) -> None:
    if instance.slug is None or instance.slug == "":
        instance.slug = slugify(
            f"{instance.id}-{instance.developer.username}-{instance.project.name}"
        )
