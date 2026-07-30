from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, Prescription


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'unit_price', 'total_price')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total', 'item_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'id')
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered', 'mark_cancelled']

    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_confirmed.short_description = "Mark selected orders as Confirmed"

    def mark_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_shipped.short_description = "Mark selected orders as Shipped"

    def mark_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_delivered.short_description = "Mark selected orders as Delivered"

    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = "Mark selected orders as Cancelled"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'created_at')
    inlines = [CartItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'total_price')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    actions = ['approve_prescriptions', 'reject_prescriptions']

    def approve_prescriptions(self, request, queryset):
        queryset.update(status='approved')
    approve_prescriptions.short_description = "Mark selected as Approved"

    def reject_prescriptions(self, request, queryset):
        queryset.update(status='rejected')
    reject_prescriptions.short_description = "Mark selected as Rejected"
