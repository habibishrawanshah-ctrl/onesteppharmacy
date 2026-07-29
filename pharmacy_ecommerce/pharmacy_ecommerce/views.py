from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.utils.translation import activate


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
