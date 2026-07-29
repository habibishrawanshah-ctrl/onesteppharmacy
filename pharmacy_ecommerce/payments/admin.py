from django.contrib import admin
from .models import PaymentMethod, Payment

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'method_type', 'is_default')
    list_filter = ('method_type',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'method_type', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'method_type')
    search_fields = ('transaction_id', 'user__username')
