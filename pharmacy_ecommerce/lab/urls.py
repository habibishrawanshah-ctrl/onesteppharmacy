from django.urls import path
from . import views

app_name = 'lab'

urlpatterns = [
    path('', views.lab_list, name='list'),
    path('<int:pk>/', views.lab_detail, name='detail'),
    path('<int:pk>/book/', views.book_lab, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
