from django import forms
from .models import PaymentMethod


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ('method_type', 'account_name', 'account_number', 'bank_name', 'is_default')


class MakePaymentForm(forms.Form):
    method = forms.IntegerField(required=False, widget=forms.HiddenInput)
    method_type = forms.ChoiceField(required=False, choices=[
        ('cash_on_delivery', 'Cash on Delivery'),
        ('credit_card', 'Credit / Debit Card'),
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('connectIPS', 'ConnectIPS'),
        ('bank_transfer', 'Bank Transfer'),
    ])
