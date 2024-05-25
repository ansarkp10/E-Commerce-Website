from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'live'), (DELETE, 'delete'))
    name = models.CharField(max_length=200)
    address = models.TextField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    email = models.EmailField(default='example@example.com')
    phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='media/', blank=True, null=True)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
