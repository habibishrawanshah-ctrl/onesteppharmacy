from django.urls import path
from . import views
from .feeds import BlogFeed

app_name = 'health'

urlpatterns = [
    path('', views.my_health_records, name='my_records'),
    path('add/', views.add_health_record, name='add'),
    path('delete/<int:pk>/', views.delete_health_record, name='delete'),
    path('conditions/', views.health_conditions, name='conditions'),
    path('blog/feed/', BlogFeed(), name='blog_feed'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
