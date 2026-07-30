from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category, Wishlist, StockNotification

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'expiry_date', 'created_at', 'image_tag')
    readonly_fields = ('image_tag',)
    fields = ('category', 'name', 'description', 'price', 'stock', 'expiry_date', 'image', 'image_tag', 'is_prescription_required', 'manufacturer')
    search_fields = ('name', 'manufacturer')
    list_filter = ('category', 'expiry_date', 'is_prescription_required')

    def image_tag(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="max-height:100px; max-width:120px;" />', obj.image.url)
        return '-'

    image_tag.short_description = 'Image Preview'

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')


@admin.register(StockNotification)
class StockNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'email', 'notified', 'created_at')
    list_filter = ('notified',)
