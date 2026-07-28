"""
URL configuration for pharmacy_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # import your home view

admin.site.site_header = "OneStep Pharmacy Administration"
admin.site.site_title = "OneStep Pharmacy Admin"
admin.site.index_title = "OneStep Pharmacy"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include('users.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('careers/', views.page_view, {'template': 'pages/careers.html'}, name='careers'),
    path('help-center/', views.page_view, {'template': 'pages/help_center.html'}, name='help_center'),
    path('shipping-info/', views.page_view, {'template': 'pages/shipping_info.html'}, name='shipping_info'),
    path('returns/', views.page_view, {'template': 'pages/returns.html'}, name='returns'),
    path('contact-us/', views.page_view, {'template': 'pages/contact_us.html'}, name='contact_us'),
    path('privacy-policy/', views.page_view, {'template': 'pages/privacy_policy.html'}, name='privacy_policy'),
    path('terms-of-service/', views.page_view, {'template': 'pages/terms_of_service.html'}, name='terms_of_service'),
    path('license-info/', views.page_view, {'template': 'pages/license_info.html'}, name='license_info'),
    path('', views.home, name='home'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

