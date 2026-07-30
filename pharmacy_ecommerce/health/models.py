from django.db import models
from django.contrib.auth.models import User

class HealthCondition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    common_medicines = models.TextField(blank=True, help_text='Comma-separated medicine names')

    def __str__(self):
        return self.name

class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    condition = models.ForeignKey(HealthCondition, on_delete=models.SET_NULL, null=True, blank=True)
    custom_condition = models.CharField(max_length=200, blank=True, help_text='If condition not in list')
    diagnosis_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    medications = models.TextField(blank=True, help_text='Current medications')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        name = self.condition.name if self.condition else self.custom_condition
        return f"{self.user.username} - {name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text='Short summary for listing')
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, help_text='e.g. Wellness, Medicine, Lifestyle')
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated tags')
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('health:blog_detail', args=[self.slug])
