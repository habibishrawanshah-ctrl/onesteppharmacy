from django.db import models
from django.contrib.auth.models import User

class LabTest(models.Model):
    CATEGORY_CHOICES = [
        ('blood', 'Blood Test'),
        ('urine', 'Urine Test'),
        ('imaging', 'Imaging / X-Ray'),
        ('cardiac', 'Cardiac'),
        ('allergy', 'Allergy Test'),
        ('general', 'General Health'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    preparation_instructions = models.TextField(blank=True, help_text='Fasting, etc.')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LabBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('sample_collected', 'Sample Collected'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_bookings')
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    preferred_time = models.CharField(max_length=50, blank=True, help_text='e.g. Morning, Afternoon')
    address = models.TextField(blank=True, help_text='Home collection address')
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    report_file = models.FileField(upload_to='lab_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lab_test.name} ({self.booking_date})"
