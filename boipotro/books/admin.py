from django.contrib import admin

# Register your models here.
from .models import Book, Author, BookList

class BookModelAdmin(admin.ModelAdmin):
	list_display = ["id","title","category"]
	list_filter = ["category", "authors","price"]

	class Meta:
		model = Book


admin.site.register(Book,BookModelAdmin)
admin.site.register(Author)
admin.site.register(BookList)
