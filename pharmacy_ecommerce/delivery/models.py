from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveries')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time_slot = models.CharField(max_length=50, blank=True, help_text='e.g. 10AM-12PM')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery #{self.order.id} - {self.status}"

class DeliveryZone(models.Model):
    name = models.CharField(max_length=100)
    districts = models.TextField(help_text='Comma-separated district names')
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    min_order_free = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    estimated_days = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
