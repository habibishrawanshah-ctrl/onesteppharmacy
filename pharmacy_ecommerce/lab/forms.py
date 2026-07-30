from django import forms
from .models import LabBooking


class LabBookingForm(forms.ModelForm):
    class Meta:
        model = LabBooking
        fields = ('booking_date', 'preferred_time', 'address', 'notes')
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
