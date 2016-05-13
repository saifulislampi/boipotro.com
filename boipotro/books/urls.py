from django.conf.urls import url

from .views import (
        home,
        all_books,
        temp_home,

    )


urlpatterns = [

    url(r'^$',temp_home),
    url(r'^all$', all_books, name='all_books'),


]
