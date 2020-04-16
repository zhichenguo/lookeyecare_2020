from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from product.models import Product


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
        # return f"{self.first_name} {self.last_name}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, related_name='orderitem', on_delete=models.CASCADE)

    # number = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cart', on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=22)
    items = models.ManyToManyField(OrderItem)

    def __str__(self):
        return self.user.username

    def get_total(self):
        return self.items.all().aggregate(order_total=Sum('product__price'))['order_total']
    
    # def products_list(self):
    #     return self.products.all()
    #
    # class Meta:
    #     verbose_name = 'Cart'
    #     verbose_name_plural = 'Carts'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    data_paid = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=100)

    def __str__(self):
        return self.stripe_charge_id

#
#
# def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
#     # after User signup, a cart and shopping list will be created automatically
#     if created:
#         Cart.objects.get_or_create(user=instance)
#
#
# # connect the signup with the actions by signal receiver
# post_save.connect(post_user_signup_receiver, sender=User)
