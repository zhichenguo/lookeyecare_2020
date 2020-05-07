from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Cart, CartItem, Order, OrderItem, Payment, Address, Coupon, Exchange, Refund


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'slug', 'quantity']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon']

    # def get_carts(self, obj):
    #     return "\n".join([c.name for c in obj.products.all()])


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'slug', 'quantity']


class ExchangeInline(admin.TabularInline):
    model = Exchange


class RefundInline(admin.TabularInline):
    model = Refund


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'ref_code', 'shipping_address', 'billing_address', 'total_amount', 'create_time', 'slug',
        'payment', 'coupon', 'coupon_saved', 'is_shipped', 'is_delivered', 'is_received',
        'exchange_requested', 'exchange_granted', 'refund_requested', 'refund_granted'
    ]
    list_display_links = ['ref_code', 'shipping_address', 'billing_address']
    list_filter = [
        'is_shipped', 'is_delivered', 'is_received',
        'exchange_requested', 'exchange_granted', 'refund_requested', 'refund_granted'
    ]
    search_fields = ['user', 'ref_code']
    inlines = [ExchangeInline, RefundInline]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'first_name',
        'last_name',
        'street_address',
        'apartment_address',
        'state',
        'zipcode',
        'address_type',
    ]
    list_filter = ['address_type', 'state']
    search_fields = ['user', 'first_name', 'last_name', 'street_address', 'apartment_address', 'city', 'zipcode']


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'coupon_type', 'amount', 'above', 'percentage', 'alive']
    list_editable = ['coupon_type', 'amount', 'above', 'percentage', 'alive']


class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['get_ref_code', 'accepted', 'email', 'create_time']
    list_editable = ['accepted']

    def get_ref_code(self, obj):
        return obj.order.ref_code

    get_ref_code.short_description = 'ref_code'


class RefundAdmin(admin.ModelAdmin):
    list_display = ['get_ref_code', 'accepted', 'email', 'create_time']
    list_editable = ['accepted']

    def get_ref_code(self, obj):
        return obj.order.ref_code

    get_ref_code.short_description = 'ref_code'


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Payment)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Exchange, ExchangeAdmin)
admin.site.register(Refund, RefundAdmin)
