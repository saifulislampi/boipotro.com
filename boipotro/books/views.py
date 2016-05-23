 # -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect

import os

from comments.forms import CommentForm
from comments.models import Comment

from .models import Book,Author
from .forms import BookUploadForm
from .epubscraper import book_keeper,imscrap


# Create your views here.





def home(request):
    new_addition=Book.objects.all().order_by("-id")[:12]
    popular=Book.objects.filter(ratings__isnull=False).order_by('-ratings__average')

    context={
        "new_addition":new_addition,
        "popular":popular,
    }
    return render(request, "index.html", context)


def all_books(request):
    return HttpResponse("<h1>This page is supposed to show all books available in the databases. </h1>")


def book_detail(request,slug=None):

    book = get_object_or_404(Book,slug=slug)
    initial_data = {
			"content_type": book.get_content_type,
			"object_id": book.id
	}
    review_form = CommentForm(request.POST or None, initial=initial_data)

    if review_form.is_valid() and request.user.is_authenticated():
        c_type = review_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = review_form.cleaned_data.get('object_id')
        content_data = review_form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()


        new_review, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj,
                            )
        return HttpResponseRedirect(new_review.content_object.get_absolute_url())


    reviews = book.comments
    context = {
        "book": book,
        "reviews" : reviews,
        "review_form" :review_form,
    }

    return render(request, "books/book-detail.html", context)


def search_suggestions(request):
    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text != u"":
            search_text = request.GET['search_text']
            search_text = search_text.strip()
            books_with_title=Book.objects.filter(title__contains=search_text)
            # post_with_content=Post.objects.filter(content__contains=search_text)

        else:
            books_with_title=[]
            # book_with_content=[]

    # post_with_title=Post.objects.filter(title__contains=search_text)

    contex_data={
        "books_with_title": books_with_title,
        # "post_with_content": post_with_content
    }
    return render(request, 'books/search-suggestions.html', contex_data)


def search_results(request):
    pass



@login_required #Deserves a better look
def add_books(request):
    context={}
    if not request.user.is_superuser:
        context["msg"]="You are not permitted to see the content of this page"
        return render(request, "books/add-books.html", context)

    if request.method=="POST":
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
            # if book_info['pubdate']:
            #     instance.published=book_info['pubdate']
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

            upload_form=BookUploadForm(request.POST or None, request.FILES or None)
            context["upload_form"]=upload_form
            context["file_upload"]=True
            context["msg"]="You just uploaded "+instance.title+" by "+author_list[0]
            return render(request, "books/add-books.html", context)

        else:
            return render(request, "books/add-books.html", context)

    else:
        upload_form=BookUploadForm(request.POST or None, request.FILES or None)
        context["upload_form"]=upload_form
        context["file_upload"]=True
        return render(request, "books/add-books.html", context)
