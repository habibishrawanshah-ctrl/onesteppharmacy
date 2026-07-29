from django.contrib import admin
from .models import HealthCondition, HealthRecord

@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'condition', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('user__username',)
