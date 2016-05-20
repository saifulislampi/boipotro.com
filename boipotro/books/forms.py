 # -*- coding: utf-8 -*-
from django import forms

from .models import Book,Author,BookList



class UploadBookFile(forms.ModelForm):

	# title=forms.CharField(label='শিরোনাম')
	# content=forms.CharField(widget=forms.Textarea,label='লেখা')

    class Meta:
        model = Book
        fields = ['book_file']
		### exclude = ['full_name']

class ConfirmBookUpload(forms.ModelForm):

	# title=forms.CharField(label='শিরোনাম')
	# content=forms.CharField(widget=forms.Textarea,label='লেখা')

    class Meta:
        model = Book
        fields = ['title','authors']
