from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Payment, Address, Coupon


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'slug', 'quantity']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'ref_code', 'coupon', 'being_delivered']

    # def get_carts(self, obj):
    #     return "\n".join([c.name for c in obj.products.all()])


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'slug']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_shipped', 'ref_code', 'create_time', 'slug']
    list_display_links = ['ref_code']


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'state',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'state']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'amount', 'above', 'percentage']


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
