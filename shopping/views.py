from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView, DetailView, View

from product.models import Product
from core.models import Profile
from .models import Cart, CartItem, Order, OrderItem, Payment, Address, Coupon, Exchange, Refund
from .forms import CheckoutForm, PaymentForm, CouponForm, ExchangeForm, RefundForm

from datetime import datetime
import time
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
    time_format = '%Y%m%d%H%M%S'
    ts = int(time.time())  # UTC timestamp
    timestamp = datetime.utcfromtimestamp(ts).strftime(time_format)
    return timestamp + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


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


class CheckoutView(LoginRequiredMixin, View):
    context_object_name = 'cart'
    template_name = 'shopping/checkout.html'

    def get(self, *args, **kwargs):
        cart = get_object_or_404(Cart, user=self.request.user)
        profile = Profile.objects.get(user=self.request.user)
        form = CheckoutForm()
        context = {
            'cart': cart,
            'profile': profile,
            'form': form,
            'couponform': CouponForm()
        }
        return render(self.request, self.template_name, context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            cart = Cart.objects.get(user=self.request.user)
            profile = Profile.objects.get(user=self.request.user)

            if form.is_valid():
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                set_default_shipping = form.cleaned_data.get('set_default_shipping')

                if use_default_shipping:
                    shipping_address = Address(
                        user=self.request.user,
                        first_name=profile.default_shipping_address.first_name,
                        last_name=profile.default_shipping_address.last_name,
                        street_address=profile.default_shipping_address.street_address,
                        apartment_address=profile.default_shipping_address.apartment_address,
                        city=profile.default_shipping_address.city,
                        state=profile.default_shipping_address.state,
                        zipcode=profile.default_shipping_address.zipcode,
                        address_type='S'
                    )

                else:
                    shipping_first_name = form.cleaned_data.get('shipping_first_name')
                    shipping_last_name = form.cleaned_data.get('shipping_last_name')
                    shipping_street_address = form.cleaned_data.get('shipping_street_address')
                    shipping_apartment_address = form.cleaned_data.get('shipping_apartment_address')
                    shipping_city = form.cleaned_data.get('shipping_city')
                    shipping_state = form.cleaned_data.get('shipping_state')
                    shipping_zipcode = form.cleaned_data.get('shipping_zipcode')
                    shipping_address = Address(
                        user=self.request.user,
                        first_name=shipping_first_name,
                        last_name=shipping_last_name,
                        street_address=shipping_street_address,
                        apartment_address=shipping_apartment_address,
                        city=shipping_city,
                        state=shipping_state,
                        zipcode=shipping_zipcode,
                        address_type='S'
                    )

                shipping_address.save()
                cart.shipping_address = shipping_address

                if set_default_shipping:
                    profile, created = Profile.objects.get_or_create(user=self.request.user)
                    profile.default_shipping_address = shipping_address
                    profile.save()

                cart.save()
                return redirect('shopping:payment')

            messages.warning(self.request, "Invalid Shipping Information")
            return redirect('shopping:checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active cart")
            return redirect('shopping:cart')


class PaymentView(LoginRequiredMixin, View):
    context_object_name = 'cart'
    template_name = 'shopping/payment.html'

    def get(self, *args, **kwargs):
        cart = get_object_or_404(Cart, user=self.request.user)
        profile = Profile.objects.get(user=self.request.user)

        # default Profile.objects.get(user=self.request.user)
        #
        # init_shipping_first_name = forms.CharField()
        # shipping_last_name = forms.CharField()
        # shipping_street_address = forms.CharField(required=False)
        # shipping_apartment_address = forms.CharField(required=False)
        # shipping_city = forms.CharField(required=False)
        # shipping_state = forms.ChoiceField(choices=CONTIGUOUS_STATES, required=False)
        # shipping_state.widget.attrs.update({'class': 'custom-select d-block w-100'})
        # shipping_zipcode = forms.CharField(required=False)
        #
        # form = PaymentForm()

        form = PaymentForm()
        if cart.shipping_address:
            context = {
                'cart': cart,
                'profile': profile,
                'form': form
            }
            return render(self.request, self.template_name, context)
        else:
            messages.warning(self.request, "Invalid Shipping Information")
            return redirect('shopping:cart')

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        try:
            # complete the order
            cart = get_object_or_404(Cart, user=self.request.user)
            profile = Profile.objects.get(user=self.request.user)
            ref_code = create_ref_code()

            if form.is_valid():
                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                set_default_billing = form.cleaned_data.get('set_default_billing')

                if use_default_billing:
                    same_billing_address = False
                    set_default_billing = False
                    billing_address = profile.default_billing_address
                elif same_billing_address:
                    use_default_billing = False
                    billing_address = Address(
                        user=self.request.user,
                        first_name=cart.shipping_address.first_name,
                        last_name=cart.shipping_address.last_name,
                        street_address=cart.shipping_address.street_address,
                        apartment_address=cart.shipping_address.apartment_address,
                        city=cart.shipping_address.city,
                        state=cart.shipping_address.state,
                        zipcode=cart.shipping_address.zipcode,
                        address_type='B'
                    )
                else:
                    billing_first_name = form.cleaned_data.get('billing_first_name')
                    billing_last_name = form.cleaned_data.get('billing_last_name')
                    billing_street_address = form.cleaned_data.get('billing_street_address')
                    billing_apartment_address = form.cleaned_data.get('billing_apartment_address')
                    billing_city = form.cleaned_data.get('billing_city')
                    billing_state = form.cleaned_data.get('billing_state')
                    billing_zipcode = form.cleaned_data.get('billing_zipcode')
                    billing_address = Address(
                        user=self.request.user,
                        first_name=billing_first_name,
                        last_name=billing_last_name,
                        street_address=billing_street_address,
                        apartment_address=billing_apartment_address,
                        city=billing_city,
                        state=billing_state,
                        zipcode=billing_zipcode,
                        address_type='B'
                    )
                billing_address.save()

                if set_default_billing:
                    profile, created = Profile.objects.get_or_create(user=self.request.user)
                    profile.default_billing_address = billing_address
                    profile.save()

                try:
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
                    payment = Payment.objects.create(
                        user=self.request.user,
                        total_amount=int(cart.get_total() * 100),
                        stripe_charge_id=charge.id  # charge.id generated by stripe
                    )
                    # payment.stripe_charge_id = charge.id  # charge.id generated by stripe
                    # payment.total_amount = int(cart.get_total() * 100)
                    payment.save()

                    # add the order to the history list
                    order = Order.objects.create(
                        user=self.request.user,
                        ref_code=ref_code,
                        payment=payment,
                        shipping_address=cart.shipping_address,
                        billing_address=billing_address,
                        coupon=cart.coupon,
                        coupon_saved=cart.get_coupon_saved(),
                        total_amount=cart.get_total()
                    )

                    for cart_item in cart.items.all():
                        order_item = OrderItem.objects.create(
                            product=cart_item.product,
                            final_price=cart_item.product.final_price,
                            quantity=cart_item.quantity
                        )
                        order.items.add(order_item)
                        cart.items.remove(cart_item)
                        cart_item.delete()

                    cart.coupon = None
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
                    print('Message is: %s' % e.error.message)
                    messages.error(self.request, f"There was a card error")
                    return redirect(reverse("shopping:payment"))
                except stripe.error.RateLimitError as e:
                    # Too many requests made to the API too quickly
                    body = e.json_body
                    err = body.get('error', {})
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
                    # TODO Something else happened, completely unrelated to Stripe. Send email to our tech
                    messages.error(
                        self.request, "There was a serious error. We are working to resolve the issue.")
                    return redirect(reverse("shopping:payment"))

            else:
                messages.warning(self.request, "Failed Payment")
                return redirect('shopping:payment')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("shopping:payment")


# def get_coupon(request, code):
#     try:
#         coupon = Coupon.objects.get(code=code)
#         if coupon is None:
#             return None
#         elif coupon.alive:
#             return coupon
#         else:
#             messages.info(request, "This coupon is expired")
#             # return Coupon.objects.none()
#             return redirect("shopping:checkout")
#     except ObjectDoesNotExist:
#         messages.info(request, "This coupon does not exist")
#         return redirect("shopping:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                cart = Cart.objects.get(user=self.request.user)
                # coupon = get_coupon(self.request, code)

                try:
                    coupon = Coupon.objects.get(code=code)
                    if coupon is None:
                        messages.info(self.request, "This coupon does not exist")
                        return redirect("shopping:checkout")
                    elif coupon.alive:
                        cart.coupon = coupon
                        cart.save()
                        messages.success(self.request, "Successfully added coupon")
                        return redirect("shopping:checkout")
                    else:
                        messages.info(self.request, "This coupon is expired")
                        # return Coupon.objects.none()
                        return redirect("shopping:checkout")
                except ObjectDoesNotExist:
                    messages.info(self.request, "This coupon does not exist")
                    return redirect("shopping:checkout")

            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("shopping:checkout")
        else:
            messages.info(self.request, "This coupon does not exist")
            return redirect("shopping:checkout")


class RequestExchangeView(View):
    def get(self, *args, **kwargs):
        form = ExchangeForm()
        context = {
            'form': form
        }
        return render(self.request, "shopping/request_exchange.html", context)

    def post(self, *args, **kwargs):
        form = ExchangeForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.exchange_requested = True
                order.save()

                # store the refund
                refund = Exchange()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("shopping:request_received")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("shopping:request_exchange")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "shopping/request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("shopping:request_received")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("shopping:request_refund")


def request_received(request):
    return render(request, 'shopping/request_received.html', {})
