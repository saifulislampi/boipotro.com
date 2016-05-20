 # -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Book,Author
from .forms import BookUploadForm
from .epubscraper import book_keeper,imscrap
import os
from django.conf import settings
# Create your views here.


def home(request):
    context={

    }
    return render(request, "index.html", context)



def all_books(request):
    return HttpResponse("<h1>This page is supposed to show all books available in the databases. </h1>")




def add_books(request):
    context={}
    if not request.user.is_staff:
        context["msg"]="You are not permitted to see the content of this page"
        return render(request, "books/add-books.html", context)

    elif request.method=="POST":
        upload_form=BookUploadForm(request.POST or None, request.FILES or None)

        if "upload" in request.POST and upload_form.is_valid():
            #Get the book instance
            instance=upload_form.save(commit=False)

            #Get Uploaded File
            file=upload_form.cleaned_data['book_file']

            #Get Book Info from epubscraper.py
            book_info=book_keeper(file)
            author_list=book_info['author'];

            #SET Info
            instance.title=book_info['title']
            instance.category=book_info['type']
            instance.published=book_info['pubdate']
            if len(book_info['subject']):
                instance.subject=book_info['subject'][0]

            #Create Book instance to get slug and other value
            instance.save();

            id=Book.objects.order_by("id").last().id
            instance = get_object_or_404(Book,id=id)

            for author in author_list:
                try:
                    auth=Author.objects.get(author_name=author)
                    instance.authors.add(auth)
                    instance.save()

                except:
                    auth=Author(author_name=author)
                    auth.save();
                    instance.authors.add(auth)
                    instance.save()


            print(instance.slug)
            image_link=book_info['cover']
            print(image_link)
            image_name=instance.slug
            imagedir=os.path.join(settings.MEDIA_ROOT,image_name)

            cover_link=imscrap(file,imagedir, image_name, image_link,False)
            cover_link=cover_link.split("/")
            cover=os.path.join(cover_link[-2],cover_link[-1])
            instance.cover=cover
            instance.save();

            context["msg"]="You just uploaded "+instance.title+" by "+author_list[0]
            return render(request, "books/add-books.html", context)

        else:
            return render(request, "books/add-books.html", context)

    else:
        upload_form=BookUploadForm(request.POST, request.FILES)
        context["upload_form"]=upload_form
        context["file_upload"]=True
        return render(request, "books/add-books.html", context)
