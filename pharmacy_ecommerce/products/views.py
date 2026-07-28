from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
