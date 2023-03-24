from django.conf import settings
from django.db import models
from django.utils import timezone


class Category(models.Model):
    def default_ordering():
        return Category.objects.count()

    name = models.CharField(max_length=200)
    is_publish = models.BooleanField(default=True)
    ordering = models.PositiveSmallIntegerField(default=default_ordering)

    def __str__(self):
        return self.name

