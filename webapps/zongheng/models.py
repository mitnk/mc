from django.db import models

class Novel(models.Model):
    title = models.CharField(max_length=40)
    book_id = models.IntegerField()
    last_id = models.IntegerField(default=0)
    last_sent = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

