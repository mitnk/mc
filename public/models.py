from django.db import models
import datetime
from django.conf import settings

APP_ROOT = settings.URL_PUBLIC

class Category(models.Model):
    title = models.CharField(max_length=40)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.pk:
            return APP_ROOT + "category/" + str(self.id) + "/"
        return ""

class Tag(models.Model):
    title = models.CharField(max_length=40)

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.pk:
            return APP_ROOT + "tag/" + str(self.id) + "/"
        return ""

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.title

    def allow_comment(self):
        age = datetime.datetime.now() - self.added
        if age.days > 90:
            return False
        return True

    def get_absolute_url(self):
        if self.pk:
            if self.slug:
                slug = self.slug.strip().lower().replace('  ', ' ').replace(' ', '_')
                return "/%s/%s/" % (self.pk, slug)
            else:
                return "/%s/" % self.pk
        return ""

class UnixCommand(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=140, blank=True, null=True)
    url = models.CharField(max_length=140)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]

