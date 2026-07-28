from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from products.models import Product


def home(request):
    featured = Product.objects.all().order_by('-created_at')[:6]
    return render(request, 'home.html', {'featured': featured})


def about(request):
    return render(request, 'about.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'users/logout.html')
