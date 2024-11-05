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

class Suppliers(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
            verbose_name = 'Supplier'
            verbose_name_plural = 'Suppliers'


# Existing models
class Delivery(models.Model):
    supplier_name = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='primary_suppliers', blank=True, null=True)
    quantity = models.PositiveIntegerField()
    date_delivered = models.DateField(auto_now_add=True)
    person_receiving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who received the asset")
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    invoice_number = models.CharField(max_length=100)
    project = models.CharField(max_length=255)
    comments = models.TextField(blank=True)
    delivery_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)  # SLK ID field

    def save(self, *args, **kwargs):
        # Generate a unique SLK ID if not already set
        if not self.delivery_id:
            # Fetch the last created Delivery instance
            last_delivery = Delivery.objects.all().order_by('id').last()
            if last_delivery:
                last_id = int(last_delivery.delivery_id[3:])  # Extract the integer part
                new_id = last_id + 1
            else:
                new_id = 1
            # Format as SLK ID (e.g., "SLK001")
            self.delivery_id = f'SLK{new_id:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Delivery {self.delivery_id} from {self.supplier_name} on {self.date_delivered}'

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
        ('faulty', 'Faulty'),
        ('onsite', 'On Site'),
        ('pending_release', 'Pending Release'),
        ('pending_approval', 'Pending Approval '),
        ('approved', 'Approved by Admin '),
    ]

    date_received = models.DateField(auto_now_add=True)
    person_receiving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who received the asset")
    asset_description = models.TextField()
    asset_description_model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    kenet_tag = models.CharField(max_length=100, unique=True)
    new_location = models.CharField(max_length=100, blank=True,null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='primary_location', blank=True, null=True)
    
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='instore',
        blank=True,
        null=True
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets', help_text="Associated delivery for this asset")

    def __str__(self):
        return f"{self.asset_description} ({self.serial_number}) ({self.kenet_tag}) ({self.location}) ({self.asset_description_model}) ({self.status}) ({self.id})({self.new_location})"

    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
            
# models.py

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.asset.serial_number}- {self.asset.status}- {self.asset.kenet_tag}- {self.asset.location}- {self.asset.id}- {self.asset.new_location}"

    class Meta:
        unique_together = ('user', 'asset')  # Ensures an asset can only be in a user's cart once


from django.db import models
from django.conf import settings

class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # items = models.ManyToManyField('Cart')  # Link to Cart items
    cart_items = models.ManyToManyField(Cart, related_name='checkouts')
    checkout_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)  # Optional remarks field

    def __str__(self):
        return f"Checkout by {self.user.username} on {self.checkout_date}"



class ReleaseFormData(models.Model):
    # Fields from the form
    name = models.CharField(max_length=255)
    date = models.DateField()
    current_location = models.CharField(max_length=255)
    new_location = models.CharField(max_length=255)
    description = models.TextField()
    quantity_required = models.PositiveIntegerField()
    quantity_issued = models.PositiveIntegerField()
    serial_number = models.CharField(max_length=100)
    kenet_tag = models.CharField(max_length=100)
    authorizing_name = models.CharField(max_length=255)
    authorization_date = models.DateField()

    # Optional: Add timestamp for when the form was submitted
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"
    
    
class AssetMovement(models.Model):
    assets = models.ManyToManyField(Assets, related_name='movements', help_text="Assets being moved")
    source_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='movement_source', help_text="Location from where the asset is being moved")
    destination_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='movement_destination', help_text="Location to where the asset is being moved")
    movement_date = models.DateTimeField(default=timezone.now, help_text="Date and time of the movement")
    person_moving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text="Person responsible for moving the asset")
    comments = models.TextField(blank=True, null=True, help_text="Additional details about the movement")

    def __str__(self):
        return f"Movement on {self.movement_date} by {self.person_moving}"

    class Meta:
        verbose_name = 'Asset Movement'
        verbose_name_plural = 'Asset Movements'
        ordering = ['-movement_date']  # Orders by most recent movements first
        

from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name="order")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
