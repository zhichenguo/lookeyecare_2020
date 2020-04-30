from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from django.db.models.signals import post_save

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


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
        # return self.get_full_name()


class CartItem(models.Model):
    product = models.ForeignKey(Product, related_name='cart_item', on_delete=models.CASCADE)
    # prescription = models.OneToOneField(Prescription)
    slug = AutoSlugField(populate_from='product', unique_with='product')

    # number = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    ref_code = models.CharField(max_length=22)

    def __str__(self):
        return self.user.username

    def get_total(self):
        return sum(item.product.final_price for item in self.items.all())

        # fuction property can not be resolved with below
        # return self.items.all().aggregate(order_total=Sum('product__final_price'))['order_total']
    #
    # class Meta:
    #     verbose_name = 'Cart'
    #     verbose_name_plural = 'Carts'


def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    # after User signup, a cart and shopping list will be created automatically
    if created:
        Cart.objects.get_or_create(user=instance)


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
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"
