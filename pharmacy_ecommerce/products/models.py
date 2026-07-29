from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

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
        if self.image and self.image.name and self.image.storage.exists(self.image.name):
            return self.image.url
        name_slug = self.name.lower().replace(' ', '_')
        from django.conf import settings
        from pathlib import Path
        static_dir = Path(settings.BASE_DIR) / 'products' / 'static' / 'images' / 'products'
        for ext in ('svg', 'jpg', 'jpeg', 'png', 'webp'):
            if (static_dir / f'{name_slug}.{ext}').exists():
                return f'{settings.STATIC_URL}images/products/{name_slug}.{ext}'
        return f'{settings.STATIC_URL}images/products/{name_slug}.svg'

    def __str__(self):
        return self.name
