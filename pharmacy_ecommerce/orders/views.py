from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from products.models import Product
from django.contrib.auth.decorators import login_required


def place_order_index(request):
    return redirect('products:list')


@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    errors = []
    if request.method == 'POST':
        raw = request.POST.get('quantity', '')
        try:
            qty = int(raw)
        except (ValueError, TypeError):
            qty = 0
            errors.append('Quantity must be a whole number.')
        if qty < 1:
            errors.append('Quantity must be at least 1.')
        elif qty > product.stock:
            errors.append(f'Only {product.stock} in stock — you requested {qty}.')
        if not errors:
            Order.objects.create(user=request.user, product=product, quantity=qty)
            product.stock -= qty
            product.save(update_fields=['stock'])
            return redirect('orders:success')
        for e in errors:
            messages.error(request, e)
    return render(request, 'orders/place_order.html', {'product': product})


def success(request):
    return render(request, 'orders/success.html')
