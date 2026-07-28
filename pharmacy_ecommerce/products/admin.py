from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price', 'stock', 'expiry_date', 'created_at', 'image_tag')
	readonly_fields = ('image_tag',)
	fields = ('name', 'description', 'price', 'stock', 'expiry_date', 'image', 'image_tag')
	search_fields = ('name',)
	list_filter = ('expiry_date',)

	def image_tag(self, obj):
		if obj.image and obj.image.name:
			return format_html('<img src="{}" style="max-height:100px; max-width:120px;" />', obj.image.url)
		return '-'

	image_tag.short_description = 'Image Preview'
