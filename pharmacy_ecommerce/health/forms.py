from django import forms
from .models import HealthRecord, HealthCondition


class HealthRecordForm(forms.ModelForm):
    custom_condition = forms.CharField(
        required=False,
        max_length=200,
        label='Or enter a custom condition',
    )

    class Meta:
        model = HealthRecord
        fields = ('condition', 'custom_condition', 'diagnosis_date', 'medications', 'notes', 'is_active')
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date'}),
            'medications': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
