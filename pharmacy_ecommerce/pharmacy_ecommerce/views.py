from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.utils.translation import activate
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum
from orders.models import Order, OrderItem
from products.models import Product
from django.utils import timezone
from datetime import timedelta
import json


def home(request):
    from products.models import Product
    featured = Product.objects.all().order_by('-created_at')[:8]
    return render(request, 'home.html', {'featured_products': featured})


def about(request):
    return render(request, 'about.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    now = timezone.now()
    last_7 = now - timedelta(days=7)
    last_30 = now - timedelta(days=30)

    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(s=Sum('total'))['s'] or 0
    total_products = Product.objects.count()
    low_stock = Product.objects.filter(stock__lt=10).count()

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    pending_orders = Order.objects.filter(status='pending').count()

    sales_data = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        day_total = Order.objects.filter(
            created_at__date=day.date()
        ).aggregate(s=Sum('total'))['s'] or 0
        sales_data.append({
            'date': day.strftime('%a'),
            'total': float(day_total),
        })

    top_products = OrderItem.objects.values(
        'product__name'
    ).annotate(total_qty=Sum('quantity')).order_by('-total_qty')[:10]

    return render(request, 'admin/dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'low_stock': low_stock,
        'recent_orders': recent_orders,
        'pending_orders': pending_orders,
        'sales_data': json.dumps(sales_data),
        'top_products': list(top_products),
    })


def page_view(request, template):
    return render(request, template)


def set_language(request):
    lang = request.GET.get('lang', 'en')
    if lang in ['en', 'ne']:
        activate(lang)
        if request.user.is_authenticated:
            profile = request.user.userprofile
            profile.preferred_language = lang
            profile.save(update_fields=['preferred_language'])
        request.session['django_language'] = lang
    return redirect(request.META.get('HTTP_REFERER', '/'))
