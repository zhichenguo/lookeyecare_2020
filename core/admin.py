from django.contrib import admin
from .models import User, Profile


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_display_links = ['username']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'default_shipping_address', 'default_billing_address']
    list_display_links = ['user']


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
