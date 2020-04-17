from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from product.models import Product


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
        # return f"{self.first_name} {self.last_name}"


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
        return self.items.all().aggregate(order_total=Sum('product__price'))['order_total']
    #
    # class Meta:
    #     verbose_name = 'Cart'
    #     verbose_name_plural = 'Carts'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='order_item', on_delete=models.CASCADE)
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
        return self.items.all().aggregate(order_total=Sum('product__price'))['order_total']


class Payment(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    data_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100)

    def __str__(self):
        return self.stripe_charge_id

#
# # after User signup, a cart and shopping list will be created automatically
# def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         Cart.objects.get_or_create(user=instance)
#
#
# # connect the signup with the actions by signal receiver
# post_save.connect(post_user_signup_receiver, sender=User)
