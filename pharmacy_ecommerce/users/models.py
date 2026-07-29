from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    preferred_language = models.CharField(max_length=5, default='en', choices=[('en', 'English'), ('ne', 'Nepali')])

    def __str__(self):
        return self.user.username
