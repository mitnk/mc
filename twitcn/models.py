from django.db import models

class ShortenUrl(models.Model):
    shorten = models.CharField(max_length=40)
    origin = models.CharField(max_length=255, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "<URL: %s>" % self.shorten

