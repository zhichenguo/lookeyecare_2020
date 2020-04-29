from django.db import models
from django.shortcuts import redirect, reverse
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.signals import post_save


class ProductQueryset(models.QuerySet):

    def instock(self):
        return self.filter(inventory__gt=0)

    def outofstock(self):
        return self.filter(inventory__lte=0)


class ProductManager(models.Manager):
    # add a property for admin use

    # def get_queryset(self):  # required
    #     return super().get_queryset()

    def get_queryset(self):  # required
        return ProductQueryset(self.model, using=self._db)

    def instock(self):
        return self.get_queryset().instock()

    def outofstock(self):
        return self.get_queryset().outofstock()


CATEGORY_CHOICES = (
    ('M', 'Men'),
    ('W', 'Women'),
    ('K', 'Kid'),
    ('S', 'Sun'),
    ('O', 'Other')
)


LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    # category = models.CharField(max_length=50, default='Frame', blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    inventory = models.IntegerField(default=0, blank=True)
    image = models.ImageField(default=0, blank=True, null=True)
    slug = AutoSlugField(populate_from='name')

    objects = ProductManager()

    def __str__(self):
        return self.name

    def is_limited(self):
        if self.price > 50:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={
            'slug': self.slug
        })

#     @property
#     def get_carts_count(self):
#         return self.cart.all().count()
#
