from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('place/', views.place_order_index, name='place_index'),
    path('place/<int:product_id>/', views.place_order, name='place'),
    path('success/', views.success, name='success'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel'),
    path('<int:order_id>/return/', views.return_order, name='return'),
    path('<int:order_id>/invoice/', views.order_invoice, name='invoice'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
]