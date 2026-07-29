from django.urls import path
from . import views

app_name = 'health'

urlpatterns = [
    path('', views.my_health_records, name='my_records'),
    path('add/', views.add_health_record, name='add'),
    path('delete/<int:pk>/', views.delete_health_record, name='delete'),
    path('conditions/', views.health_conditions, name='conditions'),
]
