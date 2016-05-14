from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book,Author
# Create your views here.


def home(request):
    return HttpResponse("<h1>This page has not been updated yet. Try some next level url. </h1>")

def temp_home(request):
    instance=Book.objects.get(id=8)
    context={
        "instance":instance,
    }
    return render(request, "index.html", context)


def all_books(request):
    return HttpResponse("<h1>This page is supposed to show all books available in the databases. </h1>")
