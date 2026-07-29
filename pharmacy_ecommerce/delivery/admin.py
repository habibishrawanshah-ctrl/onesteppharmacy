from django.contrib import admin
from .models import Delivery, DeliveryZone

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'status', 'delivery_date', 'tracking_number')
    list_filter = ('status',)
    search_fields = ('user__username', 'tracking_number')

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'delivery_fee', 'estimated_days')
    search_fields = ('name',)
