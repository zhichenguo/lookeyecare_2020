from django.contrib import admin
from .models import Product, Color, ColorsGallery, Images


class ColorsGalleryInline(admin.StackedInline):
    model = ColorsGallery
    can_delete = False


class ImagesInline(admin.StackedInline):
    model = Images
    can_delete = False


class ProductAdmin(admin.ModelAdmin):
    # can define functions with actions and methods to mulipulated price here, like on sale / discount
    # fields = ['name', 'category', 'description', 'price', 'label', 'off_percentage', 'inventory', 'image']
    list_display = ['name', 'slug', 'category', 'label', 'off_percentage', 'price', 'inventory', 'image']
    list_display_links = ['name', 'image']
    list_editable = ['category', 'label', 'off_percentage', 'price', 'inventory']
    list_filter = ['category', 'label']
    sortable_by = ['price', 'inventory']
    search_fields = ['name', 'category', 'description']
    # inlines = [ColorsGalleryInline]


class ColorsGalleryAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)
    autocomplete_fields = ('product',)
    list_display = ['product', 'color', 'slug']
    list_filter = ['color']
    search_fields = ['product__name']
    inlines = [ImagesInline]

    # def get_product_name(self, obj):
    #     return obj.product.name
    #
    # def get_color_name(self, obj):
    #     return obj.color.color_name
    #
    # get_product_name.short_description = 'product'
    # get_color_name.short_description = 'color'


admin.site.register(Color)
admin.site.register(Product, ProductAdmin)
admin.site.register(ColorsGallery, ColorsGalleryAdmin)
