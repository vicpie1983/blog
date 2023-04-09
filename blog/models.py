from django.conf import settings
from django.db import models
from django.utils import timezone

from tinymce.models import HTMLField


class Series(models.Model):
    name = models.CharField(max_length=200, verbose_name='시리즈')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='태그')

    def __str__(self):
        return self.name


class Category(models.Model):
    def default_ordering():
        return Category.objects.count()

    name = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, blank=True, null=True)
    is_publish = models.BooleanField(default=True)
    ordering = models.PositiveSmallIntegerField(default=default_ordering)
    image = models.ImageField(null=True, blank=True, upload_to='category/')

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = HTMLField(verbose_name='tinymce', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField('blog.Tag', verbose_name='태그')
    series = models.ManyToManyField('blog.Series', verbose_name='시리즈')

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

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

