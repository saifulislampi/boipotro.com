 # -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book,Author
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
        context["msg"]="You are permitted to see the content of this page"
        return render(request, "books/add-books.html", context)
