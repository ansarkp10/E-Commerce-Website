from django.db import models
from django.db.models import Q

class Product(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = (
        (LIVE, 'Live'),
        (DELETE, 'Delete')
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    image = models.ImageField(upload_to='media/')
    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    CATEGORY_CHOICES = (
        ('Men Shirts', 'Men Shirts'),
        ('Men T-Shirts', 'Men T-Shirts'),
        ('Ladies Dresses', 'Ladies Dresses'),
        ('Children dresses', 'Children dresses'),
        ('Mobiles', 'Mobiles'),  # Modified 'MObiles' to 'Mobiles'
        ('Watches', 'Watches'),
    )
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Others')

    def __str__(self):
        return self.title
    
    @classmethod
    def search(cls, query):
        return cls.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
