from django import forms
from .models import Order, OrderItem, CartItem


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    next = forms.CharField(required=False, widget=forms.HiddenInput)


class UpdateCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=0)


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Delivery Address')
    phone = forms.CharField(max_length=15, label='Phone Number')
    delivery_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Preferred Delivery Date')
    delivery_time = forms.ChoiceField(required=False, choices=[
        ('', 'Any time'),
        ('Morning (9AM-12PM)', 'Morning (9AM-12PM)'),
        ('Afternoon (12PM-5PM)', 'Afternoon (12PM-5PM)'),
        ('Evening (5PM-9PM)', 'Evening (5PM-9PM)'),
    ], label='Delivery Time')
    payment_method = forms.ChoiceField(choices=[
        ('cash_on_delivery', 'Cash on Delivery'),
        ('credit_card', 'Credit / Debit Card'),
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('connectIPS', 'ConnectIPS'),
        ('bank_transfer', 'Bank Transfer'),
    ], label='Payment Method')


class PlaceOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)


class PrescriptionForm(forms.Form):
    image = forms.ImageField(required=False, label='Upload Prescription Image')
    file = forms.FileField(required=False, label='Upload Prescription PDF')
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}), label='Doctor Notes')
