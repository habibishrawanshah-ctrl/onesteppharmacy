from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .models import Product

from django.core.paginator import Paginator

def product_list(request):
    product_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def search(request):
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        search_qs = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        ).order_by('-created_at')
        paginator = Paginator(search_qs, 12)
        page_number = request.GET.get('page')
        results = paginator.get_page(page_number)
    return render(request, 'products/search_results.html', {'results': results, 'query': q})
