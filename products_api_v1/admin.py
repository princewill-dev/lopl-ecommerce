from django.contrib import admin
from .models import Product, Pack

class ProductInline(admin.TabularInline):
    model = Product
    extra = 0

class PackAdmin(admin.ModelAdmin):
    list_display = ('pack_name', 'pack_id', 'created_at')
    ordering = ('created_at',)
    inlines = [ProductInline]

admin.site.register(Pack, PackAdmin)

# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('product_name', 'product_id', 'product_price', 'product_category', 'product_type', 'product_variants', 'image_tag')
#     ordering = ('product_name',)

#     def get_readonly_fields(self, request, obj=None):
#         if obj: # editing an existing object
#             return self.readonly_fields + ('product_id',)
#         return self.readonly_fields

#     def image_tag(self, obj):
#         if obj.product_image:
#             return mark_safe('<img src="%s" width="50" height="50" />' % (obj.product_image.url,))
#         else:
#             return 'No Image Found'
#     image_tag.short_description = 'Image'

# admin.site.register(Product, ProductAdmin)