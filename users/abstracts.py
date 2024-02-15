import uuid

from django.db import models
from cloudinary.models import CloudinaryField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UniversalIdModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        max_length=255,
    )

    class Meta:
        abstract = True


class AbstractProfile(models.Model):
    firstname = models.CharField(blank=True, max_length=500, null=True)
    lastname = models.CharField(blank=True, max_length=500, null=True)
    image = CloudinaryField("images", null=True, blank=True)
    about = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
