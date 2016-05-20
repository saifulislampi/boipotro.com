 # -*- coding: utf-8 -*-
from django import forms

from .models import Book,Author,BookList


class BookUploadForm(forms.ModelForm):
	# title=forms.CharField(label='শিরোনাম')
    class Meta:
        model = Book
        fields = ['book_file','price','free','active']
