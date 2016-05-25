# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ItemCountView,CartView
from .views import (
    cart_item_count,
    checkout,

)


urlpatterns = [

    url(r'^$',CartView.as_view(), name='cart'),
    # url(r'^$',cart, name='cart'),
    url(r'cart_item_count$', cart_item_count, name='item_count'),
    url(r'^checkout$',checkout, name='checkout'),
    # url(r'count$', ItemCountView.as_view(), name='item_count'),
    # url(r^add$', add_books, name='add_books'),
    # url(r'^(?P<slug>[\w|\W]+)/$', book_detail, name='detail'),


]
