from django.db import models

class Category(models.Model):
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
    location = models.CharField(max_length=200)
    
    # Status field with choices and default value
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='instore',  # Default to 'instore'
        blank=True,
        null=True
    )

    # New location field with blank, null, and default value
    new_location = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        default='University of Nairobi KENET STORE'
    )
    
    # Foreign key to Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.asset_description} ({self.serial_number})"
