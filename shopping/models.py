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
    ref_code = models.CharField(max_length=22)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    # payment = models.ForeignKey(
    #     'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = sum(item.get_total_final_price() for item in self.items.all())
        if self.coupon:
            if self.coupon.coupon_type == 'P':
                total *= self.coupon.percentage
            elif self.coupon.coupon_type == 'A':
                if total > self.coupon.above:
                    total -= self.coupon.amount
            elif self.coupon.coupon_type == 'M':
                total -= self.coupon.amount
        return total

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

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order', on_delete=models.CASCADE)
    is_shipped = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=22, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(OrderItem)
    slug = AutoSlugField(populate_from='ref_code', always_update=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        return sum(item.final_price for item in self.items.all())

        # fuction property can not be resolved with below
        # return self.items.all().aggregate(order_total=Sum('product__final_price'))['order_total']


class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    data_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100)

    def __str__(self):
        return self.stripe_charge_id


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    coupon_type = models.CharField(choices=COUPON_CHOICES, max_length=1)
    amount = models.FloatField(default=0, blank=True, null=True)
    above = models.FloatField(default=0, blank=True, null=True)
    percentage = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=150)
    apartment_address = models.CharField(max_length=150)
    state = models.CharField(choices=CONTIGUOUS_STATES, max_length=2)
    zip = models.CharField(max_length=22)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'
