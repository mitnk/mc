from django.db import models


class Cost(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    comment = models.CharField(max_length=40, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
