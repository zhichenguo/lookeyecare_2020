from django.contrib import admin

from .models import Product, Cart, User


class ProductAdmin(admin.ModelAdmin):
    # can define functions with actions and methods to mulipulated price
    fields = ['name', 'category', 'description', 'price', 'inventory', 'image', 'get_carts_count']
    list_display = ['name', 'category', 'description', 'price', 'inventory', 'image', 'get_carts_count']
    list_display_links = ['name', 'image']
    list_editable = ['category', 'price', 'inventory']
    list_filter = ['category']
    sortable_by = ['price', 'inventory']
    search_fields = ['name', 'category', 'description']


class CartAdmin(admin.ModelAdmin):
    list_display = ('owner', 'productId', 'number')


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(User)
