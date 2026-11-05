from cms.models import CMSPlugin
from django.db import models


class SpecTable(CMSPlugin):
    title = models.CharField(max_length=100, default="Tech specs")

    def __str__(self):
        return self.title


class SpecRow(CMSPlugin):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.label}: {self.value}"
