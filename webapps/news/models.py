from django.db import models

class News(models.Model):
    url = models.CharField(max_length=512)
    title = models.CharField(max_length=512, blank=True, null=True)
    points = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    filed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-added"]

    def __str__(self):
        return self.title
    __unicode__ = __str__
    __repr__ = __str__
