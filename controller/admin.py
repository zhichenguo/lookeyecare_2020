from django.contrib import admin
from .models import User, Order, OrderItem, Payment


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name']
    list_display_links = ['username', 'first_name', 'last_name']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_ordered', 'ref_code']

    # def get_carts(self, obj):
    #     return "\n".join([c.name for c in obj.products.all()])


admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
