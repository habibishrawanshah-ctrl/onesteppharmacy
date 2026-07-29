from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.my_deliveries, name='my_deliveries'),
    path('track/<int:pk>/', views.delivery_tracking, name='tracking'),
    path('zones/', views.delivery_zones, name='zones'),
]
