from django.db import models

class Note(models.Model):
    url = models.CharField(max_length=128, blank=True, null=True)
    text = models.CharField(max_length=1024)
    remark = models.CharField(max_length=128, blank=True, null=True)
    book = models.CharField(max_length=128, blank=True, null=True)
    author = models.CharField(max_length=128, blank=True, null=True)
    added = models.DateTimeField()

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.text

class Word(models.Model):
    url = models.CharField(max_length=128, blank=True, null=True)
    word = models.CharField(max_length=64)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.word
