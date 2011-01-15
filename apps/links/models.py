from django.db import models

class Link(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=512)

    def __unicode__(self):
        return self.name

