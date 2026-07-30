from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import PaymentMethod, Payment

@login_required
def payment_methods(request):
    methods = PaymentMethod.objects.filter(user=request.user)
    return render(request, 'payments/methods.html', {'methods': methods})

@login_required
def add_payment_method(request):
    if request.method == 'POST':
        method_type = request.POST.get('method_type')
        account_name = request.POST.get('account_name', '').strip()
        account_number = request.POST.get('account_number', '').strip()
        bank_name = request.POST.get('bank_name', '').strip()
        is_default = request.POST.get('is_default') == 'on'
        if not method_type:
            messages.error(request, 'Please select a payment method.')
        else:
            if is_default:
                PaymentMethod.objects.filter(user=request.user).update(is_default=False)
            PaymentMethod.objects.create(
                user=request.user,
                method_type=method_type,
                account_name=account_name,
                account_number=account_number,
                bank_name=bank_name,
                is_default=is_default,
            )
            messages.success(request, 'Payment method added!')
            return redirect('payments:methods')
    return render(request, 'payments/add_method.html')

@login_required
def delete_payment_method(request, pk):
    method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    method.delete()
    messages.success(request, 'Payment method removed.')
    return redirect('payments:methods')

@login_required
def make_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    methods = PaymentMethod.objects.filter(user=request.user)
    if request.method == 'POST':
        method_id = request.POST.get('method')
        if method_id:
            method = get_object_or_404(PaymentMethod, pk=method_id, user=request.user)
            method_type = method.method_type
        else:
            method = None
            method_type = request.POST.get('method_type', 'cash_on_delivery')
        Payment.objects.create(
            order=order,
            user=request.user,
            amount=order.total,
            method=method,
            method_type=method_type,
            status='completed',
            transaction_id=f'TXN{order.id:06d}',
        )
        messages.success(request, f'Payment of NPR {order.total} completed!')
        return redirect('orders:success')
    return render(request, 'payments/make_payment.html', {'order': order, 'methods': methods})
