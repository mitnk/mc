from django.db import models
import datetime
from django.conf import settings

APP_ROOT = settings.URL_PUBLIC

class Category(models.Model):
    title = models.CharField(max_length=40)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.pk:
            return APP_ROOT + "category/" + str(self.id) + "/"
        return ""

class Article(models.Model):
    """#TODO: Update Category and Tag informations when 
        using delete_selected actions in admin site.
        But It's not a big deal, because every delete or save action
        will do a complete thing for this updating.
    """
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)

    class Meta:
        ordering = ["-added"]

    def __unicode__(self):
        return self.title

    def allow_comment(self):
        age = datetime.datetime.now() - self.added
        if age.days > 90:
            return False
        return True

    def get_absolute_url(self):
        if self.pk:
            if self.slug:
                slug = self.slug.strip().lower().replace('  ', ' ').replace(' ', '_')
                return "/%s/%s/" % (self.pk, slug)
            else:
                return "/%s/" % self.pk
        return ""

    def delete(self, *args, **kwargs):
        """Update Category and Tag informations"""
        self.category.count = Article.objects.filter(category=self.category).count() - 1
        self.category.save()
        super(Article, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Update Category and Tag informations when INSERT.

           Note that, tags should always write correctly for that tag counts at INSERT,
           but later-updated tags will work for search actions.
        """
        if not self.pk:
            self.category.count = Article.objects.filter(category=self.category).count() + 1
            self.category.save()

        super(Article, self).save(*args, **kwargs)

class UnixCommand(models.Model):
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=140, blank=True, null=True)
    url = models.CharField(max_length=140)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]

