from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView, DetailView, View

from product.models import Product
from .models import Cart, CartItem, Order, OrderItem, Payment
import stripe
import string
import random

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderListView(ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'shopping/orders_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-create_time')


class OrderDetailView(DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'shopping/order_detail.html'


def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


@login_required
def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart_item = CartItem.objects.create(product=product)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.add(cart_item)
    cart.save()
    messages.info(request, product.name + ' is added to your cart')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def add_quantity(request, cart_item_slug):
    cart_item = get_object_or_404(CartItem, slug=cart_item_slug)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the order
        if cart.items.filter(slug=cart_item.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shopping:cart")
        else:
            cart.items.add(cart_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shopping:cart")
    else:
        cart = Cart.objects.create(user=request.user)
        cart.items.add(cart_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shopping:cart")


@login_required
def remove_from_cart(request, cart_item_slug):
    cart_item = get_object_or_404(CartItem, slug=cart_item_slug)
    cart_qs = Cart.objects.filter(user=request.user)

    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the order
        if cart.items.filter(slug=cart_item.slug).exists():
            cart.items.remove(cart_item)
            cart_item.delete()
            cart.save()
            messages.info(request, cart_item.product.name + " successfully removed from your cart.")
            return redirect("shopping:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shopping:cart")
    else:
        messages.info(request, "You do not have an active cart")
        return redirect("shopping:cart")


@login_required
def minus_quantity(request, cart_item_slug):
    cart_item = get_object_or_404(CartItem, slug=cart_item_slug)
    cart_qs = Cart.objects.filter(user=request.user)
    if cart_qs.exists():
        cart = cart_qs[0]
        # check if the cart item is in the order
        if cart.items.filter(slug=cart_item.slug).exists():
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart.items.remove(cart_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shopping:cart")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shopping:cart")
    else:
        messages.info(request, "You do not have an active cart")
        return redirect("shopping:cart")


class CartView(LoginRequiredMixin, ListView):
    model = Cart
    context_object_name = 'cart'
    template_name = 'shopping/cart.html'

    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        context = {
            'cart': cart
        }
        return render(request, self.template_name, context)


@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    context = {
        'cart': cart
    }
    return render(request, 'shopping/cart.html', context)


@login_required
def thankyou(request):
    return render(request, 'shopping/thankyou.html', {})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == "POST":

        try:
            # complete the order
            cart.ref_code = create_ref_code()

            # create stripe charge
            # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
            token = request.POST.get('stripeToken')
            charge = stripe.Charge.create(
                amount=int(cart.get_total() * 100),  # in cents, need to times 100
                currency="usd",
                source=token,  # obtained with Stripe.js
                description=f"Charge for {request.user.username}",
            )

            # create our payment object and link to the order
            payment = Payment()
            payment.cart = cart
            payment.stripe_charge_id = charge.id  # charge.id generated by stripe
            payment.total_amount = cart.get_total()
            payment.save()

            # add the order to the history list
            order = Order.objects.create(
                user=request.user,
                ref_code=cart.ref_code,
                # payment_id=payment.stripe_charge_id
            )

            for cart_item in cart.items.all():
                order_item = OrderItem.objects.create(
                    product=cart_item.product,
                    final_price=cart_item.product.final_price
                )
                order.items.add(order_item)
                cart.items.remove(cart_item)
                cart_item.delete()
            order.save()
            cart.save()

            # redirect to a thank you page with continue shopping
            return redirect(reverse('shopping:thankyou'))

        # send email to yourself
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            # print('Status is: %s' % e.http_status)
            # print('Type is: %s' % e.error.type)
            # print('Code is: %s' % e.error.code)
            # # param is '' in this case
            # print('Param is: %s' % e.error.param)
            # print('Message is: %s' % e.error.message)
            messages.error(request, "There was a card error.")
            return redirect(reverse("shopping:checkout"))
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(request, "There was a rate limit error on Stripe.")
            return redirect(reverse("shopping:checkout"))
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(request, "Invalid parameters for Stripe request.")
            return redirect(reverse("shopping:checkout"))
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(request, "Invalid Stripe API keys.")
            return redirect(reverse("shopping:checkout"))
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(request, "There was a network error. Please try again.")
            return redirect(reverse("shopping:checkout"))
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send yourself an email
            messages.error(request, "There was an error. Please try again.")
            return redirect(reverse("shopping:checkout"))
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(
                request, "There was a serious error. We are working to resolve the issue.")
            return redirect(reverse("shopping:checkout"))

    context = {
        'cart': cart
    }
    return render(request, 'shopping/checkout.html', context)


class CheckoutView(LoginRequiredMixin, View):
    context_object_name = 'cart'
    template_name = 'shopping/checkout.html'

    def get(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)

        context = {
            'cart': cart
        }
        return render(request, 'shopping/checkout.html', context)


class PaymentView(LoginRequiredMixin, View):
    context_object_name = 'cart'
    template_name = 'shopping/payment.html'

    def get(self, *args, **kwargs):
        cart = get_object_or_404(Cart, user=self.request.user)

        context = {
            'cart': cart
        }
        return render(self.request, 'shopping/payment.html', context)

    def post(self, *args, **kwargs):
        cart = get_object_or_404(Cart, user=self.request.user)
        try:
            # complete the order
            cart.ref_code = create_ref_code()

            # create stripe charge
            # `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
            token = self.request.POST.get('stripeToken')
            charge = stripe.Charge.create(
                amount=int(cart.get_total() * 100),  # in cents, need to times 100
                currency="usd",
                source=token,  # obtained with Stripe.js
                description=f"Charge for {self.request.user.username}",
            )

            # create our payment object and link to the order
            payment = Payment()
            payment.cart = cart
            payment.stripe_charge_id = charge.id  # charge.id generated by stripe
            payment.total_amount = cart.get_total()
            payment.save()

            # add the order to the history list
            order = Order.objects.create(
                user=self.request.user,
                ref_code=cart.ref_code,
                # payment_id=payment.stripe_charge_id
            )

            for cart_item in cart.items.all():
                order_item = OrderItem.objects.create(
                    product=cart_item.product,
                    final_price=cart_item.product.final_price
                )
                order.items.add(order_item)
                cart.items.remove(cart_item)
                cart_item.delete()
            order.save()
            cart.save()

            # redirect to a thank you page with continue shopping
            return redirect(reverse("shopping:thankyou"))

        # send email to yourself
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            # print('Status is: %s' % e.http_status)
            # print('Type is: %s' % e.error.type)
            # print('Code is: %s' % e.error.code)
            # # param is '' in this case
            # print('Param is: %s' % e.error.param)
            # print('Message is: %s' % e.error.message)
            messages.error(self.request, "There was a card error.")
            return redirect(reverse("shopping:payment"))
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "There was a rate limit error on Stripe.")
            return redirect(reverse("shopping:payment"))
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters for Stripe request.")
            return redirect(reverse("shopping:payment"))
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Invalid Stripe API keys.")
            return redirect(reverse("shopping:payment"))
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "There was a network error. Please try again.")
            return redirect(reverse("shopping:payment"))
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send yourself an email
            messages.error(self.request, "There was an error. Please try again.")
            return redirect(reverse("shopping:payment"))
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(
                self.request, "There was a serious error. We are working to resolve the issue.")
            return redirect(reverse("shopping:payment"))
