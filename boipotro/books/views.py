 # -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book,Author
from .forms import UploadBookFile,ConfirmBookUpload
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

    else:
        if "upload" in request.POST:
            confirm_form=ConfirmBookUpload()
            context["confirm_form"]=confirm_form
            context['confirm_upload']=True
            context["msg"]="You are permitted to see the content of this page and you clicked upload"
            return render(request, "books/add-books.html", context)

        elif "confirm" in request.POST:
            context["msg"]="You are permitted to see the content of this page and you clicked confirm"
            return render(request, "books/add-books.html", context)

        else:
            form=UploadBookFile()
            context["form"]=form
            context["file_upload"]=True
            return render(request, "books/add-books.html", context)
