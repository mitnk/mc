from django.db import models

class WebAppInfo(models.Model):
    category = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.category + "-" + self.name

class FavoTweet(models.Model):
    name = models.CharField(max_length=40)
    text = models.CharField(max_length=160)
    tweet_id = models.CharField(max_length=24, null=True, blank=True)
    added = models.DateTimeField()

    class Meta:
        ordering = ["-added"]
