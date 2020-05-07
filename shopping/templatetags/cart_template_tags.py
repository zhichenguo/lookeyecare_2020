from django import template
from shopping.models import Cart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter
def cart_total_saving(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user)
        if qs.exists():
            cart = qs[0]
            return cart.get_total_save_in_cart()
    return 0
