from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    # can define functions with actions and methods to mulipulated price here, like on sale / discount
    fields = ['name', 'category', 'description', 'price', 'inventory', 'image']
    list_display = ['name', 'slug', 'category', 'label', 'off_percentage', 'price', 'inventory', 'image']
    list_display_links = ['name', 'image']
    list_editable = ['category', 'label', 'off_percentage', 'price', 'inventory']
    list_filter = ['category', 'label']
    sortable_by = ['price', 'inventory']
    search_fields = ['name', 'category', 'description']


admin.site.register(Product, ProductAdmin)
