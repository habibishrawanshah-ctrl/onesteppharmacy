from django import forms
from .models import UserInsurance, InsuranceProvider


class UserInsuranceForm(forms.ModelForm):
    class Meta:
        model = UserInsurance
        fields = ('provider', 'policy_number', 'coverage_type', 'start_date', 'end_date')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
