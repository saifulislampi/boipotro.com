# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
        home,
        all_books,
        add_books,
        book_detail,
        search_suggestions,
        search_results,
    )


urlpatterns = [

    url(r'^$',home),
    url(r'^all$', all_books, name='all_books'),
    url(r'^add$', add_books, name='add_books'),
    url(r'^(?P<slug>[\w|\W]+)/$', book_detail, name='detail'),
    url(r'^search_suggestions$',search_suggestions , name='search_suggestions'),
    url(r'^search_results$',search_results , name='search_results'),


]
