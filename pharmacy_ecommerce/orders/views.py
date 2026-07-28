from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order
from products.models import Product
from django.contrib.auth.decorators import login_required
from .cart import add_to_cart, remove_from_cart, update_quantity, cart_items


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


def cart_view(request):
    items, total = cart_items(request)
    return render(request, 'orders/cart.html', {'items': items, 'total': total})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get('quantity', 1))
    add_to_cart(request, product_id, qty)
    messages.success(request, f'{product.name} added to cart.')
    return redirect(request.POST.get('next', 'cart'))


def cart_remove(request, product_id):
    remove_from_cart(request, product_id)
    return redirect('cart')


def cart_update(request, product_id):
    qty = int(request.POST.get('quantity', 0))
    update_quantity(request, product_id, qty)
    return redirect('cart')


@login_required
def checkout(request):
    items, total = cart_items(request)
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        for item in items:
            if item['quantity'] > item['product'].stock:
                messages.error(request, f'Only {item["product"].stock} of {item["product"].name} in stock.')
                return render(request, 'orders/checkout.html', {'items': items, 'total': total})
            Order.objects.create(
                user=request.user,
                product=item['product'],
                quantity=item['quantity'],
            )
            item['product'].stock -= item['quantity']
            item['product'].save(update_fields=['stock'])
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, 'Order placed successfully!')
        return redirect('orders:success')
    return render(request, 'orders/checkout.html', {'items': items, 'total': total})
