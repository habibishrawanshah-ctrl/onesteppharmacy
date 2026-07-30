from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<int:pk>/', views.product_detail, name='detail'),
    path('search/', views.search, name='search'),
    path('search/autocomplete/', views.search_autocomplete, name='autocomplete'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('stock-notify/<int:product_id>/', views.stock_notify, name='stock_notify'),
]
