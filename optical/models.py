from django.contrib.auth.models import User
from django.db import models

GENDER_CHOICES = (
    # max length = 1, use get_status_display() to return the display value
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Not Available')
)


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True)

    # birth_date = models.DateField()
    def __str__(self):
        return self.username

    @property
    def full_name(self):  # call without ()
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default='Frame', blank=True)
    description = models.TextField(default='', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    inventory = models.IntegerField(default=0, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_limited(self):
        if self.price > 50:
            return True
        else:
            return False


class Cart(models.Model):
    # on_delete=CASCADE: product bei shan le, zhe tiao zi dong shan
    # null=True: ru guo you, productId shi kong ye bu hui bao cuo
    productId = models.ForeignKey(Product, related_name='carts', on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    owner = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE, null=True)
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['create_time']
