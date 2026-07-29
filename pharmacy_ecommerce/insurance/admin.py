from django.contrib import admin
from .models import InsuranceProvider, UserInsurance

@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_phone', 'is_active')
    search_fields = ('name',)

@admin.register(UserInsurance)
class UserInsuranceAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'policy_number', 'coverage_type', 'is_active')
    list_filter = ('coverage_type', 'is_active')
    search_fields = ('user__username', 'policy_number')
