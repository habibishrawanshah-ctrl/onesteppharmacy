import os
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)
    is_prescription_required = models.BooleanField(default=False)
    manufacturer = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        if self.image and self.image.name:
            name = self.image.name
            if name.startswith(('http://', 'https://')):
                return name
            if self.image.storage.exists(name):
                return self.image.url
        name_slug = self.name.lower().replace(' ', '_')
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'cxfqn4a3')
        return f'https://res.cloudinary.com/{cloud_name}/image/upload/v1/products/{name_slug}.jpg'

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} \u2764 {self.product.name}"


class StockNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_notifications')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_notifications')
    email = models.EmailField()
    notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} notify when {self.product.name} in stock"
