from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import redirect, reverse
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.signals import post_save


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username
        # return f"{self.first_name} {self.last_name}"


# GENDER_CHOICES = (
#     # max length = 1, use get_status_display() to return the display value
#     ('M', 'Male'),
#     ('F', 'Female'),
#     ('O', 'Other'),
#     ('N', 'Not Available')
# )


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


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default='Frame', blank=True)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    inventory = models.IntegerField(default=0, blank=True)
    image = models.ImageField(blank=True, null=True)
    # slug = models.SlugField()
    slug = AutoSlugField(populate_from='name', always_update=True)

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
