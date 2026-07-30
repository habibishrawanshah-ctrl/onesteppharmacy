from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(
                user=user,
                defaults={'address': '', 'phone': ''},
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product', 'delivery')
    return render(request, 'users/profile.html', {'orders': orders})
