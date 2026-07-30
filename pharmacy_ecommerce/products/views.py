from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from .models import Product, Category
from reviews.models import Review

def product_list(request):
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort = request.GET.get('sort', '-created_at')

    qs = Product.objects.all()

    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    if min_price:
        qs = qs.filter(price__gte=min_price)

    if max_price:
        qs = qs.filter(price__lte=max_price)

    sort_options = {
        '-created_at': 'Newest',
        'price': 'Price: Low to High',
        '-price': 'Price: High to Low',
        'name': 'Name: A-Z',
        '-name': 'Name: Z-A',
    }
    if sort in sort_options:
        qs = qs.order_by(sort)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'active_category': category_slug,
        'active_sort': sort,
        'sort_options': sort_options,
        'min_price': min_price,
        'max_price': max_price,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    if not related.exists():
        related = Product.objects.exclude(pk=pk)[:4]

    recommended = Product.objects.all().order_by('-created_at')[:4]
    popular = Product.objects.annotate(order_count=Count('orderitem')).order_by('-order_count')[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'review_count': reviews.count(),
        'related_products': related,
        'recommended_products': recommended,
        'popular_products': popular,
        'star_range': range(5),
    })


def search(request):
    q = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    results = []

    if q:
        search_qs = Product.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(manufacturer__icontains=q)
        )

        if category_slug:
            search_qs = search_qs.filter(category__slug=category_slug)
        if min_price:
            search_qs = search_qs.filter(price__gte=min_price)
        if max_price:
            search_qs = search_qs.filter(price__lte=max_price)

        search_qs = search_qs.order_by('-created_at')
        paginator = Paginator(search_qs, 12)
        page_number = request.GET.get('page')
        results = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'products/search_results.html', {
        'results': results,
        'query': q,
        'categories': categories,
        'active_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
    })
