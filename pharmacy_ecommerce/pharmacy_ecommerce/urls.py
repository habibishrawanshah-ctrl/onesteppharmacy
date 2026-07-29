from django.contrib import admin
from django.urls import path, include
from . import views
from orders import views as orders_views

admin.site.site_header = "OneStep Pharmacy Administration"
admin.site.site_title = "OneStep Pharmacy Admin"
admin.site.index_title = "OneStep Pharmacy"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('set-language/', views.set_language, name='set_language'),

    # Products
    path('products/', include('products.urls')),

    # Orders
    path('orders/', include('orders.urls')),
    path('cart/', orders_views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', orders_views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', orders_views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', orders_views.cart_update, name='cart_update'),
    path('checkout/', orders_views.checkout, name='checkout'),

    # Labs
    path('lab/', include('lab.urls')),

    # Reviews
    path('reviews/', include('reviews.urls')),

    # Health
    path('health/', include('health.urls')),

    # Delivery
    path('delivery/', include('delivery.urls')),

    # Insurance
    path('insurance/', include('insurance.urls')),

    # Payments
    path('payments/', include('payments.urls')),

    # Users
    path('users/', include('users.urls')),

    # Pages
    path('careers/', views.page_view, {'template': 'pages/careers.html'}, name='careers'),
    path('help-center/', views.page_view, {'template': 'pages/help_center.html'}, name='help_center'),
    path('shipping-info/', views.page_view, {'template': 'pages/shipping_info.html'}, name='shipping_info'),
    path('returns/', views.page_view, {'template': 'pages/returns.html'}, name='returns'),
    path('contact-us/', views.page_view, {'template': 'pages/contact_us.html'}, name='contact_us'),
    path('privacy-policy/', views.page_view, {'template': 'pages/privacy_policy.html'}, name='privacy_policy'),
    path('terms-of-service/', views.page_view, {'template': 'pages/terms_of_service.html'}, name='terms_of_service'),
    path('license-info/', views.page_view, {'template': 'pages/license_info.html'}, name='license_info'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
