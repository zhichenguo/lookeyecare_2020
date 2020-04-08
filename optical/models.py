from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default='Frame')
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    inventory = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    # on_delete=CASCADE: product bei shan le, zhe tiao zi dong shan
    # null=True: ru guo you, productId wei kong ye bu hui bao cuo
    productId = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    owner = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE, null=True)


