 # -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, Http404, JsonResponse
from books.models import Book,Author
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Cart,CartItem

from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView


def cart_item_count(request):
    if request.method=="GET":
        print("Item count request is GET")
        if request.is_ajax():
            print("Item count request is AJAX")
            cart_id =request.session.get("cart_id")
            if cart_id == None:
                count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                count = cart.items.count()
            request.session["cart_item_count"] = count
            return JsonResponse({"count": count})
        else:
            raise Http404
    else:
        raise Http404



# Create your views here.
#NOT USING IT//Using cart_item_count instead

class ItemCountView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			cart_id = self.request.session.get("cart_id")
			if cart_id == None:
				count = 0
			else:
				cart = Cart.objects.get(id=cart_id)
				count = cart.items.count()
			request.session["cart_item_count"] = count
			return JsonResponse({"count": count})
		else:
			raise Http404

class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = "carts/cart.html"

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0) #5 minutes
        cart_id = self.request.session.get("cart_id")
        if cart_id == None:
            cart = Cart()
            cart.tax_percentage = 0.075
            cart.save()
            cart_id = cart.id
            self.request.session["cart_id"] = cart_id
        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
        item_id = request.GET.get("item")
        delete_item = request.GET.get("delete", False)
        flash_message = ""
        item_added = False

        if item_id:
            item_instance = get_object_or_404(Book, id=item_id)
            qty = request.GET.get("qty", 1)
            try:
                if int(qty) < 1:
                    delete_item = True
            except:
                raise Http404
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)

            if created:
                flash_message = "আপনার নির্বাচিত বইটি কার্টে যুক্ত করা হয়েছ।"
                item_added = True
            if delete_item:
                flash_message = "বইটি কার্ট থেকে বাদ দেয়া হয়েছে।"
                cart_item.delete()
            else:
                if not created:
                    flash_message = "আপনার নির্বাচিত বইটি আগেই কার্টে যুক্ত করা হয়েছ।"
                cart_item.quantity = qty
                cart_item.save()
            if not request.is_ajax():
                return HttpResponseRedirect(reverse("carts:cart"))
				#return cart_item.cart.get_absolute_url()

        if request.is_ajax():
            try:
                total = cart_item.line_item_total
            except:
                total = None
            try:
                subtotal = cart_item.cart.subtotal
            except:
                subtotal = None

            try:
                cart_total = cart_item.cart.total
            except:
                cart_total = None

            try:
                tax_total = cart_item.cart.tax_total
            except:
                tax_total = None

            try:
                total_items = cart_item.cart.items.count()
            except:
                total_items = 0

            data = {
                    "deleted": delete_item,
                    "item_added": item_added,
                    "line_total": total,
                    "subtotal": subtotal,
                    "cart_total": cart_total,
                    "tax_total": tax_total,
                    "flash_message": flash_message,
                    "total_items": total_items
                    }

            return JsonResponse(data)


        context = {
            "object": self.get_object()
        }
        template = self.template_name
        return render(request, template, context)





def cart(request):
    msg="Cart has not been implemented yet!"
    context={
        "msg":msg,

    }
    return render(request, "carts/cart.html", context)
