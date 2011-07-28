from django.db import models

class WebAppInfo(models.Model):
    category = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    value = models.CharField(max_length=255, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.category + "-" + self.name

