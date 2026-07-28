from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        results = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        ).order_by('-created_at')
    return render(request, 'products/search_results.html', {'results': results, 'query': q})
