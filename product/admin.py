from django.contrib import admin
from .models import Product, Category, Image, Coupon


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'image_tag',
        'price',
        'quantity',
        'description',
        'slug',
        'date_added',
        'category',
        'in_stock',
    )
    search_fields = (
        'title',
        'slug',
        'description',
        'price',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('images', 'image')

    def images(self, obj):
        return obj.title


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'limited',
        'active',
        'discount',
        'valid_to',
        'valid_from',
        'used',
        'product',
    )
    search_fields = ('code',)
