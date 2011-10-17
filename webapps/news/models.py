from django.db import models

class News(models.Model):
    url = models.CharField(max_length=512, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    points = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.title

    def is_home_page(self):
        return '/' not in self.url.replace('//', '').strip('/')
