from django.contrib import admin
from .models import Product, Variant, ProductImage, ProductVariant, ProductVariantPrice

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','sku','created_at', 'updated_at')

admin.site.register(Product, ProductAdmin)

class VariantAdmin(admin.ModelAdmin):
    list_display = ('title','created_at', 'updated_at')

admin.site.register(Variant, VariantAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('file_path','created_at', 'updated_at')

admin.site.register(ProductImage, ProductImageAdmin)

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('variant','created_at', 'updated_at')

admin.site.register(ProductVariant, ProductVariantAdmin)

class ProductVariantPriceAdmin(admin.ModelAdmin):
    list_display = ('price','stock','created_at', 'updated_at')

admin.site.register(ProductVariantPrice, ProductVariantPriceAdmin)