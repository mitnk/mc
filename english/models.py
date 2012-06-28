from django.db import models

class Acceptation(models.Model):
    word = models.CharField(max_length=30)
    acceptation = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
