from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from shopping.models import Address


# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return self.username
        # return self.get_full_name()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    default_shipping_address = models.ForeignKey(Address, related_name='default_shipping_address',
                                                 on_delete=models.CASCADE, blank=True, null=True)
    default_billing_address = models.ForeignKey(Address, related_name='default_billing_address',
                                                on_delete=models.CASCADE, blank=True, null=True)


def post_user_signup_receiver(sender, instance, created, *args, **kwargs):
    # after User signup, a profile will be created automatically
    if created:
        user_profile = Profile.objects.get_or_create(user=instance)


# connect the signup with the actions by signal receiver
post_save.connect(post_user_signup_receiver, sender=settings.AUTH_USER_MODEL)

# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
#     one_click_purchasing = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.username
