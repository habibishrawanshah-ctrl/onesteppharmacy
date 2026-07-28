from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
