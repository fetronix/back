from django.db import models
from django.utils import timezone

class Delivery(models.Model):
    supplier_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    date_delivered = models.DateField(default=timezone.now)  # Automatically set to the current date
    person_receiving = models.CharField(max_length=255)
    invoice_file = models.FileField(upload_to='invoices/')  # Specify the directory for file uploads
    invoice_number = models.CharField(max_length=100)
    project = models.CharField(max_length=255)
    comments = models.TextField(blank=True)  # Optional field for comments

    def __str__(self):
        return f'Delivery from {self.supplier_name} on {self.date_delivered}'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Assets(models.Model):
    STATUS_CHOICES = [
        ('instore', 'In Store'),
        ('tested', 'Tested'),
        ('default', 'Default'),
        ('onsite', 'On Site'),
        ('pending_release', 'Pending Release'),
    ]

    date_received = models.DateField(auto_now_add=True)  # Automatically set to the current date
    person_receiving = models.CharField(max_length=100)
    asset_description = models.TextField()
    serial_number = models.CharField(max_length=100, unique=True)
    kenet_tag = models.CharField(max_length=100, unique=True)
    # Foreign key to the Location model for the primary location
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='primary_location', blank=True, null=True)
    
    # Foreign key to the same Location model for the new location
    new_location = models.ForeignKey(Location, on_delete=models.SET_NULL, related_name='new_location', blank=True, null=True)

    
    # Status field with choices and default value
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='instore',  # Default to 'instore'
        blank=True,
        null=True
    )

    # Foreign key to Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.asset_description} ({self.serial_number})"
