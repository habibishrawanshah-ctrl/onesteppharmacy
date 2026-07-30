from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem, Prescription
from products.models import Product
from django.contrib.auth.decorators import login_required
from .cart import add_to_cart, remove_from_cart, update_quantity, cart_items, clear_cart, get_or_create_cart
from delivery.models import Delivery
from payments.models import Payment
from users.models import UserProfile
from utils.email import send_order_confirmation, send_welcome_email
import logging

logger = logging.getLogger(__name__)


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
            total = product.price * qty
            order = Order.objects.create(
                user=request.user,
                total=total,
                shipping_address='',
                phone='',
            )
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=qty,
                unit_price=product.price,
                total_price=total,
            )
            product.stock -= qty
            product.save(update_fields=['stock'])

            profile = getattr(request.user, 'userprofile', None)
            if not profile:
                profile, _ = UserProfile.objects.get_or_create(
                    user=request.user, defaults={'address': '', 'phone': ''}
                )

            Delivery.objects.create(
                order=order,
                user=request.user,
                address=profile.address or 'Pending',
                phone=profile.phone or '0000000000',
            )

            Payment.objects.create(
                order=order,
                user=request.user,
                amount=total,
                method_type='cash_on_delivery',
                status='pending',
            )

            send_order_confirmation(order)
            if not request.user.last_login:
                send_welcome_email(request.user)
            logger.info(f'Order #{order.id} placed by {request.user.username}')
            return redirect('orders:success')
        for e in errors:
            messages.error(request, e)
    return render(request, 'orders/place_order.html', {'product': product})


def success(request):
    return render(request, 'orders/success.html')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status not in ('pending', 'confirmed'):
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('users:profile')

    if request.method == 'POST':
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save(update_fields=['stock'])
        order.status = 'cancelled'
        order.save(update_fields=['status'])
        logger.info(f'Order #{order.id} cancelled by {request.user.username}')
        messages.success(request, f'Order #{order.id} has been cancelled.')
        return redirect('users:profile')

    return render(request, 'orders/cancel_confirm.html', {'order': order})


@login_required
def return_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.status != 'delivered':
        messages.error(request, 'Only delivered orders can be returned.')
        return redirect('users:profile')

    if request.method == 'POST':
        reason = request.POST.get('reason', '').strip()
        order.notes = (order.notes or '') + f'\nReturn reason: {reason}'
        order.status = 'returned'
        order.save(update_fields=['status', 'notes'])
        logger.info(f'Order #{order.id} return requested by {request.user.username}: {reason}')
        messages.success(request, f'Return request for Order #{order.id} has been submitted.')
        return redirect('users:profile')

    return render(request, 'orders/return_form.html', {'order': order})


@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})


def cart_view(request):
    if request.user.is_authenticated:
        items, total = cart_items(request.user)
        shipping = 100 if total < 500 else 0
        grand_total = total + shipping
        return render(request, 'orders/cart.html', {
            'items': items,
            'total': total,
            'shipping': shipping,
            'grand_total': grand_total,
        })
    return render(request, 'orders/cart.html', {
        'items': [],
        'total': 0,
        'shipping': 0,
        'grand_total': 0,
    })


def cart_add(request, product_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to add items to cart.')
        return redirect('login')
    product = get_object_or_404(Product, pk=product_id)
    qty = int(request.POST.get('quantity', 1))
    add_to_cart(request.user, product_id, qty)
    messages.success(request, f'{product.name} added to cart.')
    logger.info(f'{request.user} added {product.name} to cart')
    return redirect(request.POST.get('next', 'cart'))


def cart_remove(request, product_id):
    if request.user.is_authenticated:
        remove_from_cart(request.user, product_id)
    return redirect('cart')


def cart_update(request, product_id):
    if request.user.is_authenticated:
        qty = int(request.POST.get('quantity', 0))
        update_quantity(request.user, product_id, qty)
    return redirect('cart')


@login_required
def checkout(request):
    items, total = cart_items(request.user)
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')

    shipping = 100 if total < 500 else 0
    grand_total = total + shipping
    has_prescription_items = any(
        item.product.is_prescription_required for item in items
    )

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()[:15]
        delivery_date = request.POST.get('delivery_date', '')
        delivery_time = request.POST.get('delivery_time', '')
        payment_method = request.POST.get('payment_method', 'cash_on_delivery')

        errors = []
        if not address or not phone:
            errors.append('Please provide both shipping address and phone number.')

        if has_prescription_items:
            pres_image = request.FILES.get('prescription_image')
            pres_file = request.FILES.get('prescription_file')
            if not pres_image and not pres_file:
                errors.append(
                    'Some items in your cart require a prescription. '
                    'Please upload your prescription.'
                )

        for item in items:
            if item.quantity > item.product.stock:
                errors.append(
                    f'Only {item.product.stock} of {item.product.name} in stock.'
                )

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'orders/checkout.html', {
                'items': items, 'total': total,
                'shipping': shipping, 'grand_total': grand_total,
                'has_prescription_items': has_prescription_items,
            })

        profile, _ = UserProfile.objects.get_or_create(
            user=request.user, defaults={'address': '', 'phone': ''}
        )
        profile.address = address
        profile.phone = phone
        profile.save()

        order = Order.objects.create(
            user=request.user,
            total=grand_total,
            shipping_address=address,
            phone=phone,
            delivery_date=delivery_date or None,
            delivery_time_slot=delivery_time,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.product.price * item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=['stock'])

        if has_prescription_items:
            Prescription.objects.create(
                user=request.user,
                order=order,
                image=request.FILES.get('prescription_image'),
                file=request.FILES.get('prescription_file'),
                notes=request.POST.get('prescription_notes', ''),
            )

        Delivery.objects.create(
            order=order,
            user=request.user,
            address=address,
            phone=phone,
            delivery_date=delivery_date or None,
            delivery_time_slot=delivery_time,
        )

        Payment.objects.create(
            order=order,
            user=request.user,
            amount=grand_total,
            method_type=payment_method,
            status='pending' if payment_method == 'cash_on_delivery' else 'completed',
        )

        clear_cart(request.user)
        send_order_confirmation(order)
        if not request.user.last_login:
            send_welcome_email(request.user)
        messages.success(request, 'Order placed successfully!')
        return redirect('orders:success')

    return render(request, 'orders/checkout.html', {
        'items': items,
        'total': total,
        'shipping': shipping,
        'grand_total': grand_total,
        'has_prescription_items': has_prescription_items,
    })
