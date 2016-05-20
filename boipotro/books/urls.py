# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
        home,
        all_books,
        add_books,
        book_detail,
    )


urlpatterns = [

    url(r'^$',home),
    url(r'^all$', all_books, name='all_books'),
    url(r'^add$', add_books, name='add_books'),
    url(r'^(?P<slug>[\w|\W]+)/$', book_detail, name='detail'),
    

]
