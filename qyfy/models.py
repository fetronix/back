# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRoles(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    NETWORK_ADMIN = 'network_admin', 'Network Admin'
    NOC_USER = 'noc_user', 'NOC User'
    SYSTEM_ADMIN = 'system_admin', 'System Admin'
    NETWORK_ENGINEER = 'network_engineer', 'Network Engineer'

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.NOC_USER  # Default role can be changed as needed
    )

    def __str__(self):
        return self.username  # or return self.email if you prefer

    def clean(self):
        super().clean()  # Call the parent class's clean method
        if self.email and not self.email.endswith('@kenet.or.ke'):
            raise ValidationError("Email must be in the format 'user@kenet.or.ke'.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This calls the clean method to validate
        super().save(*args, **kwargs)  # Call the parent class's save method

    class Meta:
            verbose_name = 'User'
            verbose_name_plural = 'Users'

# Existing models
class Delivery(models.Model):
    supplier_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    date_delivered = models.DateField(auto_now_add=True)
    person_receiving = models.CharField(max_length=255)
    invoice_file = models.FileField(upload_to='invoices/')
    invoice_number = models.CharField(max_length=100)
    project = models.CharField(max_length=255)
    comments = models.TextField(blank=True)

    def __str__(self):
        return f'Delivery from {self.supplier_name} on {self.date_delivered}'
    
    
    class Meta:
            verbose_name = 'Delivery'
            verbose_name_plural = 'Deliveries'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
            verbose_name = 'Category'
            verbose_name_plural = 'Categories'

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
            verbose_name = 'Location'
            verbose_name_plural = 'Locations'

class Assets(models.Model):
    STATUS_CHOICES = [
        ('instore', 'In Store'),
        ('tested', 'Tested'),
        ('default', 'Default'),
        ('onsite', 'On Site'),
        ('pending_release', 'Pending Release'),
    ]

    date_received = models.DateField(auto_now_add=True)
    person_receiving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,help_text="User who received the asset")
    asset_description = models.TextField()
    serial_number = models.CharField(max_length=100, unique=True)
    kenet_tag = models.CharField(max_length=100, unique=True)
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='primary_location', blank=True, null=True)
    new_location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='new_location', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='instore',
        blank=True,
        null=True
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.asset_description} ({self.serial_number})"

    class Meta:
            verbose_name = 'Asset'
            verbose_name_plural = 'Assets'
            
            
            
from django.conf import settings

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    new_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)  # Link to the Location model
    
    def __str__(self):
        return f"{self.asset.asset_description}"
    
    class Meta:
            verbose_name = 'Cart'
            verbose_name_plural = 'Cart'