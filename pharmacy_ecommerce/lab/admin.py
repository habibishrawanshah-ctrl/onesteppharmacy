from django.contrib import admin
from .models import LabTest, LabBooking

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)

@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'lab_test', 'booking_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'lab_test__name')
