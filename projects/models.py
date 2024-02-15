from django.db import models

from users.abstracts import TimeStampedModel, UniversalIdModel

class Project(UniversalIdModel, TimeStampedModel):
    name = models.CharField(min_length=1)
