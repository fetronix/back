from django.db import models

# Create your models here.
from django.db import models

class Assets(models.Model):
    date_received = models.DateField(auto_now_add=True)  # Automatically set to the current date
    person_receiving = models.CharField(max_length=100)
    asset_description = models.TextField()
    serial_number = models.CharField(max_length=100, unique=True)
    kenet_tag = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.asset_description} ({self.serial_number})"
