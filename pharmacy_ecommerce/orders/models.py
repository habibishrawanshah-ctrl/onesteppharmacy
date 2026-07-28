from django.db import models
from products.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')],
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

