from django import forms
from .models import Product


class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search')
    category = forms.IntegerField(required=False, widget=forms.HiddenInput)
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Min'}))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Max'}))
    sort = forms.ChoiceField(required=False, choices=[
        ('', 'Default'),
        ('price', 'Price: Low to High'),
        ('-price', 'Price: High to Low'),
        ('name', 'Name: A-Z'),
        ('-name', 'Name: Z-A'),
        ('-created_at', 'Newest'),
    ])
