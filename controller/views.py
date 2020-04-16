from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from product.models import Product
from .models import Order, OrderItem


class HomeView(TemplateView):
    # View for home page of site.
    template_name = 'home.html'


def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    order_item = OrderItem.objects.create(product=product)
    order, created = Order.objects.get_or_create(user=request.user)
    order.items.add(order_item)
    order.save()
    messages.info(request, product.name + ' is added to your cart')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def remove_from_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    order_item = get_object_or_404(OrderItem, product=product)
    order = get_object_or_404(Order, user=request.user)
    order.items.remove(order_item)
    order.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def cart_view(request):
    order = get_object_or_404(Order, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'cart.html', context)
