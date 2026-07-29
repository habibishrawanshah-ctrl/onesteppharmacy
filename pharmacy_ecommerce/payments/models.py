from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class PaymentMethod(models.Model):
    METHOD_CHOICES = [
        ('credit_card', 'Credit / Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('khalti', 'Khalti'),
        ('esewa', 'eSewa'),
        ('connectIPS', 'ConnectIPS'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('mobile_banking', 'Mobile Banking'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method_type = models.CharField(max_length=50, choices=METHOD_CHOICES)
    account_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_method_type_display()}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    method_type = models.CharField(max_length=50, choices=PaymentMethod.METHOD_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} - {self.order.id} ({self.status})"
