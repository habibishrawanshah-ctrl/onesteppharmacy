from django.db import models
from django.contrib.auth.models import User

class InsuranceProvider(models.Model):
    name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    coverage_details = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserInsurance(models.Model):
    COVERAGE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('family', 'Family'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_policies')
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=50, choices=COVERAGE_CHOICES, default='basic')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'policy_number')

    def __str__(self):
        return f"{self.user.username} - {self.provider.name} ({self.policy_number})"
