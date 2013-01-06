import datetime
from django.db import models
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.title

    def allow_comment(self):
        return False

    def get_absolute_url(self):
        if self.pk:
            return settings.URL_WIKI + str(self.id) + "/"
        return ""
