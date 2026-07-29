from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('methods/', views.payment_methods, name='methods'),
    path('methods/add/', views.add_payment_method, name='add_method'),
    path('methods/delete/<int:pk>/', views.delete_payment_method, name='delete_method'),
    path('pay/<int:order_id>/', views.make_payment, name='make_payment'),
]
