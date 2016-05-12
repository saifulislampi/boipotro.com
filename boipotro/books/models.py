from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone

from django.utils.text import slugify

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    # PostModel = instance.__class__
    # new_id = PostModel.objects.order_by("id").last().id + 1
    new_id=""
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object,
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)

class Author(models.Model):
    author_name=models.CharField(max_length=255)
    books=models.ManyToManyField('Book',blank=True)

    def __unicode__(self):
        return self.author_name

    def __str__(self):
        return self.author_name


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author', blank=True)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=120,blank=True)
    subject = models.CharField(max_length=120, blank=True)
    cover = models.ImageField(upload_to=upload_location)
    book_file = models.FileField(upload_to=upload_location)
    book_type = models.CharField( max_length=120, default="ebook")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
