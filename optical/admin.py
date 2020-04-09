from django.contrib import admin

from .models import Product, Cart, User


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description', 'price', 'inventory')


class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'productId', 'number')


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(User)
