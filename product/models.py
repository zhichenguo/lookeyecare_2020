from django.db import models
from django.shortcuts import redirect, reverse
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.signals import post_save
# from taggit.managers import TaggableManager


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
    ('S', 'On Sale'),
    ('N', 'New')
)

SIZE_CHOICES = (
    ('SM', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('NA', 'NA')
)

SHAPE_CHOICES = (
    ('RT', 'Rectangle'),
    ('RD', 'Round'),
    ('A', 'Aviator'),
    ('G', 'Geometric'),
    ('NA', 'NA')
)


# COLOR_CHOICES = (
#     ('BK', 'Black'),
#     ('B', 'Blue'),
#     ('R', 'Red'),
#     ('G', 'Green'),
#     ('NA', 'NA')
# )

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'products/{0}/{1}'.format(instance.name, filename)


def color_sample_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'colors/{0}_sample_{1}'.format(instance.color_name, filename)


class Color(models.Model):
    color_name = models.CharField(max_length=22)
    sample = models.ImageField(upload_to=color_sample_directory_path, blank=True, null=True)

    def __str__(self):
        return self.color_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    description = models.TextField(default='', blank=True)
    size = models.CharField(default='NA', choices=SIZE_CHOICES, max_length=2)
    shape = models.CharField(default='NA', choices=SHAPE_CHOICES, max_length=2)
    price = models.FloatField(default=0, blank=True, null=True)
    inventory = models.IntegerField(default=0, blank=True)

    # image = models.ImageField(upload_to=image_directory_path, default=0, blank=True, null=True)
    # image = models.ImageField(
    #     upload_to=image_directory_path,
    #     default=0, blank=True, null=True
    # )

    slug = AutoSlugField(populate_from='name', unique=True, editable=False)

    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    off_percentage = models.FloatField(default=0, blank=True, null=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def is_limited(self):
        if self.price > 50:
            return True
        else:
            return False

    @property
    def final_price(self):
        if self.label == 'S':
            return self.price * (1 - self.off_percentage)
        else:
            return self.price

    def get_absolute_url(self):
        return reverse("product:product_detail", kwargs={
            'slug': self.slug
        })


#     @property
#     def get_carts_count(self):
#         return self.cart.all().count()
#


def get_color_gallery_slug(instance):
    return '{0}_{1}'.format(instance.product, instance.color)


class ColorsGallery(models.Model):
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, related_name='colors_gallery', on_delete=models.CASCADE)

    slug = AutoSlugField(populate_from=get_color_gallery_slug, unique=True, editable=False)

    def __str__(self):
        return self.product.name + '' + self.color.color_name


def gallery_images_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'products/{0}/{1}_{2}'.format(
        instance.color_gallery.product.name, instance.color_gallery.color.color_name, filename)


class Images(models.Model):
    color_gallery = models.ForeignKey(ColorsGallery, related_name='images', on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=gallery_images_directory_path, verbose_name='Image')
