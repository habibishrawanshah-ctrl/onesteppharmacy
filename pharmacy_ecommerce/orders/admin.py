from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'product__name')
    date_hierarchy = 'order_date'
