from django.contrib import admin

# Register your models here.
from .models import Cart, CartItem



class CartItemInline(admin.TabularInline):
	model = CartItem

class CartAdmin(admin.ModelAdmin):
	list_display = ["id","user","total"]
	list_filter = ["user",]

	inlines = [
		CartItemInline
	]
	class Meta:
		model = Cart


class CartItemAdmin(admin.ModelAdmin):
	list_display = ["item","cart","line_item_total"]
	list_filter = ["item","cart"]
	class Meta:
		model = CartItem

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
