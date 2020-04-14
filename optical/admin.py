from django.contrib import admin

from .models import Product, Cart, User


class ProductAdmin(admin.ModelAdmin):
    # can define functions with actions and methods to mulipulated price here, like on sale / discount
    fields = ['name', 'category', 'description', 'price', 'inventory', 'image']
    list_display = ['name', 'slug', 'category', 'price', 'inventory', 'image', 'get_carts_count']
    list_display_links = ['name', 'image']
    list_editable = ['category', 'price', 'inventory']
    list_filter = ['category']
    sortable_by = ['price', 'inventory']
    search_fields = ['name', 'category', 'description']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_carts']

    def get_carts(self, obj):
        return "\n".join([c.name for c in obj.products.all()])


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_display_links = ['username', 'first_name', 'last_name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(User, UserAdmin)
