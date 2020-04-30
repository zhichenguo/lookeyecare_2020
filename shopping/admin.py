from django.contrib import admin
from .models import User, Cart, CartItem, Order, OrderItem, Payment


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_display_links = ['username', 'first_name', 'last_name']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'slug']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user']

    # def get_carts(self, obj):
    #     return "\n".join([c.name for c in obj.products.all()])


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'slug']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_shipped', 'ref_code', 'create_time', 'slug']
    list_display_links = ['ref_code']


admin.site.register(User, UserAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment)
