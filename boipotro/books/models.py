# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating

from comments.models import Comment

#MY Custom Libraries
from .convert_to_bangla import convert_number_in_bangla

# from django.utils.text import slugify

#A function for creating simple unicode slug
def sslugify(line):
    ret="";
    temp= line.strip()
    for i in range(0,len(temp)):
        if temp[i]==' ':
            ret=ret+'-'
        else:
            ret=ret+temp[i]

    return ret




def upload_location(instance, filename):

    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.slug, instance.slug,extension)

def author_upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.author_name, instance.author_name,extension)


class Author(models.Model):
    author_name=models.CharField(max_length=255)
    slug = models.CharField(unique=True, max_length=255)

    #EXTRA
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to=author_upload_location,null=True,blank=True)
    external_link=models.TextField(null=True,blank=True)


    def __unicode__(self):
        return self.author_name

    def __str__(self):
        return self.author_name

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"slug": self.slug})


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField('Author', blank=True)
    slug = models.CharField(unique=True, max_length=255)
    category = models.CharField(max_length=120,null=True,blank=True) ##Type In catalog
    subject = models.CharField(max_length=120, null=True,blank=True)
    #Files
    cover = models.ImageField(upload_to=upload_location,null=True,blank=True)
    book_file = models.FileField(upload_to=upload_location)
    book_type = models.CharField( max_length=120, default="Ebook",blank=True)

    #Times
    published = models.DateField(auto_now=False, auto_now_add=False, null=True,blank=True) #will be CHANGE
    added = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    updated = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    #Price
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True,blank=True, default=0.00)
    free = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    #For Rating Purpose
    ratings = GenericRelation(Rating, related_query_name='books')


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_price(self):
        if self.free or self.price==None:
            return 0;
        return self.price

    def get_price_in_bn(self):
        return convert_number_in_bangla(self.get_price())

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"slug": self.slug})

    def add_to_cart(self):
        return "%s?item=%s&qty=1" %(reverse("carts:cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("carts:cart"), self.id)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type




class BookList(models.Model):
    list_name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True) ##It should not be blank
    books = models.ManyToManyField(Book)




def create_slug(instance, new_slug=None):
    slug = sslugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Book.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_book_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_book_receiver, sender=Book)




def create_author_slug(instance, new_slug=None):
    slug = sslugify(instance.author_name)
    if new_slug is not None:
        slug = new_slug
    qs = Author.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_author_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_author_slug(instance)

pre_save.connect(pre_save_author_receiver, sender=Author)
