from django.contrib.auth.models import User
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=40)
    isbn = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ""

class Read(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    page = models.IntegerField(blank=True, null=True)
    mark = models.IntegerField(blank=True, null=True)
    update = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"<%s> are reading <%s> (%s/%s)" % (self.user, self.book, self.mark, self.page)

