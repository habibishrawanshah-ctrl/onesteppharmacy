from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('place/', views.place_order_index, name='place_index'),
    path('place/<int:product_id>/', views.place_order, name='place'),
    path('success/', views.success, name='success'),
]