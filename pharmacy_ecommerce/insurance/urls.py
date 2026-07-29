from django.urls import path
from . import views

app_name = 'insurance'

urlpatterns = [
    path('', views.my_insurance, name='my_insurance'),
    path('add/', views.add_insurance, name='add'),
    path('delete/<int:pk>/', views.delete_insurance, name='delete'),
    path('providers/', views.provider_list, name='providers'),
]
