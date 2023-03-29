from django.conf import settings
from django.db import models
from django.utils import timezone

from tinymce.models import HTMLField


class Category(models.Model):
    def default_ordering():
        return Category.objects.count()

    name = models.CharField(max_length=200)
    is_publish = models.BooleanField(default=True)
    ordering = models.PositiveSmallIntegerField(default=default_ordering)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = HTMLField(verbose_name='tinymce', blank=True)
    #text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

