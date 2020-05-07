from django.db import models
from django.db.models import Sum
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.signals import post_save
from localflavor.us.us_states import CONTIGUOUS_STATES, US_STATES

from product.models import Product

GENDER_CHOICES = (
    # max length = 1, use get_status_display() to return the display value
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Not Available')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

COUPON_CHOICES = (
    ('P', 'PERCENTAGE'),
    ('A', 'ABOVE'),
    # ('B', 'BOGO'),
    ('M', 'AMOUNT')
)


class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name='cart_item', on_delete=models.CASCADE)
    # prescription = models.OneToOneField(Prescription)
    slug = AutoSlugField(populate_from='product', unique_with='product')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_total_final_price(self):
        return self.quantity * self.product.final_price

    def get_amount_saved(self):
        return self.get_total_product_price() - self.get_total_final_price()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    shipping_address = models.ForeignKey(
        'Address', related_name='cart_shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='cart_billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_save_in_cart(self):
        return sum(item.get_amount_saved() for item in self.items.all())

    def get_total(self):
        total = sum(item.get_total_final_price() for item in self.items.all())
        if self.coupon:
            if self.coupon.coupon_type == 'P':
                total *= 1 - self.coupon.percentage
            elif self.coupon.coupon_type == 'A':
                if total > self.coupon.above:
                    total -= self.coupon.amount
            elif self.coupon.coupon_type == 'M':
                total -= self.coupon.amount
        return total

    def get_coupon_saved(self):
        total = sum(item.get_total_final_price() for item in self.items.all())
        saved = 0
        if self.coupon:
            if self.coupon.coupon_type == 'P':
                saved = total * self.coupon.percentage
            elif self.coupon.coupon_type == 'A':
                if total > self.coupon.above:
                    saved = self.coupon.amount
            elif self.coupon.coupon_type == 'M':
                saved = self.coupon.amount
        return saved

        # fuction property can not be resolved with below
        # return self.items.all().aggregate(order_total=Sum('product__final_price'))['order_total']


def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    # after User signup, a cart and shopping list will be created automatically
    if created:
        user_cart = Cart.objects.get_or_create(user=instance)


# connect the signup with the actions by signal receiver
post_save.connect(post_user_signup_receiver, sender=settings.AUTH_USER_MODEL)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='order_item', on_delete=models.CASCADE)
    final_price = models.FloatField(default=0, blank=True, null=True)
    # prescription = models.OneToOneField(Prescription)
    slug = AutoSlugField(populate_from='product', unique_with='product')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name

    def get_total_final_price(self):
        return self.quantity * self.final_price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order', on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=22, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(OrderItem)
    shipping_address = models.ForeignKey(
        'Address', related_name='order_shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='order_billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    coupon_saved = models.FloatField(default=0, blank=True, null=True)
    total_amount = models.FloatField()
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    exchange_requested = models.BooleanField(default=False)
    exchange_granted = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='ref_code', always_update=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        # total price without coupon
        return sum(item.get_total_final_price() for item in self.items.all())

        # fuction property can not be resolved with below
        # return self.items.all().aggregate(order_total=Sum('product__final_price'))['order_total']


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payment', on_delete=models.CASCADE)
    total_amount = models.FloatField()
    data_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100)

    def __str__(self):
        return self.stripe_charge_id


class Coupon(models.Model):
    code = models.CharField(max_length=22)
    coupon_type = models.CharField(choices=COUPON_CHOICES, max_length=1)
    amount = models.FloatField(default=0, blank=True, null=True)
    above = models.FloatField(default=0, blank=True, null=True)
    percentage = models.FloatField(default=0, blank=True, null=True)
    alive = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class Exchange(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.ref_code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order.ref_code


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    street_address = models.CharField(max_length=150)
    apartment_address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(choices=CONTIGUOUS_STATES, max_length=2)
    zipcode = models.CharField(max_length=22)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
