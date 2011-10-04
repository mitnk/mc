from django.db import models


class User(models.Model):
    douban_id = models.CharField(max_length=20)
    name = models.CharField(max_length=160, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return self.douban_id


class Book(models.Model):
    subject_id = models.CharField(max_length=20)
    title = models.CharField(max_length=160, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.title

class Read(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    total = models.IntegerField(default=0, blank=True, null=True)
    current = models.IntegerField(default=0, blank=True, null=True)
    update = models.DateTimeField(auto_now=True)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-update"]

    def get_absolute_url(self):
        return "/douqian/read/%s/" % self.id

    def get_edit_url(self):
        return "/douqian/read/%s/edit/" % self.id

    def __unicode__(self):
        if not self.total or not self.current:
            return u"<%s> are reading <%s>" % (self.user, self.book)
        return u"<%s> are reading <%s> (%s)" % (self.user, self.book, self.current/self.total)
