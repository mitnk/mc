from django.db import models

class Dict(models.Model):
    word = models.CharField(max_length=30, unique=True)
    pos = models.CharField(max_length=30, blank=True)
    pron = models.CharField(max_length=255, blank=True)
    acceptation = models.CharField(max_length=255)
    define = models.TextField(blank=True)
    gloss = models.CharField(max_length=512, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    orig = models.CharField(max_length=512, blank=True)
    trans = models.CharField(max_length=512, blank=True)
