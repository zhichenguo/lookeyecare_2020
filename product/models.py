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
    ('C', 'Contact'),
    ('S', 'Sun'),
    ('O', 'Other')
)

GENDER_CHOICES = (
    ('M', 'Men'),
    ('W', 'Women'),
    ('K', 'Kid'),
    ('U', 'Unisex'),
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


class BaseCurve(models.Model):
    bc = models.DecimalField(decimal_places=1, max_digits=2)

    def __str__(self):
        return str(self.bc)


class Diameter(models.Model):
    dia = models.FloatField()

    def __str__(self):
        return str(self.dia)


class Power(models.Model):
    power = models.FloatField()

    def __str__(self):
        return str(self.power)


class Cylinder(models.Model):
    cyl = models.FloatField()

    def __str__(self):
        return str(self.cyl)


class Axis(models.Model):
    axis = models.IntegerField()

    def __str__(self):
        return str(self.axis)


class HighLow(models.Model):
    hl = models.CharField(max_length=50)

    def __str__(self):
        return self.hl


class DN(models.Model):
    dn = models.CharField(max_length=50)

    def __str__(self):
        return self.dn


class AddOnPower(models.Model):
    add = models.CharField(max_length=22)

    def __str__(self):
        return self.add


class ContactColor(models.Model):
    cc = models.CharField(max_length=50)

    def __str__(self):
        return self.cc


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(default='O', choices=CATEGORY_CHOICES, max_length=1)
    gender = models.CharField(default='U', choices=GENDER_CHOICES, max_length=1, blank=True)
    short_description = models.CharField(max_length=120, default='', blank=True)
    description = models.TextField(default='', blank=True)
    size = models.CharField(default='NA', choices=SIZE_CHOICES, max_length=2, blank=True)
    shape = models.CharField(default='NA', choices=SHAPE_CHOICES, max_length=2, blank=True)
    price = models.FloatField(default=0, blank=True)
    inventory = models.IntegerField(default=0, blank=True)

    # # contact data fields
    # base_curve = models.ManyToManyField(BaseCurve, default=None, blank=True, null=True)
    # diameter = models.ManyToManyField(Diameter, blank=True, null=True)
    # power = models.ManyToManyField(Power, blank=True, null=True)
    # cylinder = models.ManyToManyField(Cylinder, blank=True, null=True)
    # axis = models.ManyToManyField(Axis, blank=True, null=True)
    # high_low = models.ManyToManyField(HighLow, blank=True, null=True)
    # dn = models.ManyToManyField(DN, blank=True, null=True)
    # add_on_power = models.ManyToManyField(AddOnPower, blank=True, null=True)
    # contact_color = models.ManyToManyField(ContactColor, blank=True, null=True)

    # image = models.ImageField(upload_to=image_directory_path, default=0, blank=True, null=True)

    slug = AutoSlugField(populate_from='name', unique=True, editable=False)
    label = models.CharField(default='P', choices=LABEL_CHOICES, max_length=1, blank=True)
    off_percentage = models.FloatField(default=0, blank=True)
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
        instance.color_gallery.product.name,
        instance.color_gallery.color.color_name, filename)


class Images(models.Model):
    color_gallery = models.ForeignKey(ColorsGallery, related_name='images', on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to=gallery_images_directory_path, verbose_name='Image')


class Contact(Product):
    # name = models.CharField(max_length=100)
    # # category = models.CharField(default='C', choices=CATEGORY_CHOICES, max_length=1)
    # # gender = models.CharField(default='U', choices=GENDER_CHOICES, max_length=1, blank=True)
    # short_description = models.CharField(max_length=120, default='', blank=True)
    # description = models.TextField(default='', blank=True)
    # # size = models.CharField(default='NA', choices=SIZE_CHOICES, max_length=2, blank=True)
    # # shape = models.CharField(default='NA', choices=SHAPE_CHOICES, max_length=2, blank=True)
    # price = models.FloatField(default=0, blank=True)
    # inventory = models.IntegerField(default=0, blank=True)
    # slug = AutoSlugField(populate_from='name', unique=True, editable=False)
    # label = models.CharField(default='P', choices=LABEL_CHOICES, max_length=1, blank=True)
    # off_percentage = models.FloatField(default=0, blank=True)
    # objects = ProductManager()

    # contact data fields
    base_curve = models.ManyToManyField(BaseCurve, default=None, blank=True, null=True)
    diameter = models.ManyToManyField(Diameter, blank=True, null=True)
    power = models.ManyToManyField(Power, blank=True, null=True)
    cylinder = models.ManyToManyField(Cylinder, blank=True, null=True)
    axis = models.ManyToManyField(Axis, blank=True, null=True)
    high_low = models.ManyToManyField(HighLow, blank=True, null=True)
    dn = models.ManyToManyField(DN, blank=True, null=True)
    add_on_power = models.ManyToManyField(AddOnPower, blank=True, null=True)
    contact_color = models.ManyToManyField(ContactColor, blank=True, null=True)

    # image = models.ImageField(upload_to=image_directory_path, default=0, blank=True, null=True)
