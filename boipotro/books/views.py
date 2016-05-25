 # -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q

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
        "nbar":"home",
    }
    return render(request, "index.html", context)


def all_books(request):

    books=Book.objects.all()
    category=[]

    for book in books:
        if book.category not in category:
            category.append(book.category)

    context={

        "nbar":"all",
        "books": books,
        "category": category,
        "priority": "all",
    }
    if request.method=="GET":
        try:
            p=request.GET.get('p',"")
            print(p)

            if(p=="time"):
                books=Book.objects.all().order_by("-id");
                context["priority"]="time"
                context["books"]=books
            elif(p=="free"):
                books=Book.objects.filter(free=True).order_by("-id")
                context["books"]=books
                context["priority"]="free"
            elif(p=="popular"):
                books=Book.objects.filter(ratings__isnull=False).order_by('-ratings__average')
                context["books"]=books
                context["priority"]="popular"
            elif p!="":
                books=Book.objects.filter(category=p).order_by("-id")
                context["books"]=books
                context["priority"]=p
        except:
            pass
        return render(request, "books/all-books.html", context)

    return render(request, "books/all-books.html", context)


def all_author(request):
    authors=Author.objects.all();
    context={
        "authors":authors,
        "nbar":"author",
    }

    return render(request, "books/all-author.html", context)




def author_detail(request,slug=None):
    author = get_object_or_404(Author,slug=slug)
    print(author)
    context={
        "author":author,
        "nbar":"author",
    }

    return render(request, "books/author-detail.html", context)



def book_detail(request,slug=None):

    book = get_object_or_404(Book,slug=slug)

    auth=book.authors.all()[0];

    print(auth)

    same_author_and_category=auth.book_set.all().filter(category=book.category)
    same_author=auth.book_set.all()
    same_category=Book.objects.filter(category=book.category)


    related=[]

    for rbook in same_author_and_category:
        if rbook.id!=book.id:
            print(rbook)
            related.append(rbook)

    if len(related)<8:
        for  rbook in same_author:
            if rbook.id!=book.id and rbook not in related:
                related.append(rbook)

    if len(related)<8:
        for  rbook in same_category:
            if rbook.id!=book.id and rbook not in related:
                related.append(rbook)

    related=related[:8]


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
        "related":related,
    }

    return render(request, "books/book-detail.html", context)


def search_suggestions(request):

    if request.method == "GET":
        search_text = request.GET['search_text']
        if search_text is not None and search_text !=u"":
            search_text = search_text.strip()
            books_with_title=Book.objects.filter(title__icontains=search_text)
            authors_with_name=Author.objects.filter(author_name__icontains=search_text)
            books_with_category=Book.objects.filter(category__icontains=search_text)


        else:
            books_with_title=[]
            authors_with_name=[]
            books_with_category=[]
            # book_with_content=[]

    # post_with_title=Post.objects.filter(title__contains=search_text)

    contex_data={
        "books_with_title": books_with_title,
        "authors_with_name": authors_with_name,
        "books_with_category": books_with_category,
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
