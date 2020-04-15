from django.db import models

# class Cart(models.Model):
#     products = models.ManyToManyField(Product, related_name='cart')
#     user = models.OneToOneField(User, related_name='carts', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.username
#
#     def products_list(self):
#         return self.products.all()
#
#     class Meta:
#         verbose_name = 'Cart'
#         verbose_name_plural = 'Carts'
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
