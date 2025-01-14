# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import base64
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.conf import settings



class UserRoles(models.TextChoices):
    CAN_VIEW = 'can_view', 'Can View'
    CAN_VERIFY_ITEMS = 'can_checkout_items', 'Can Checkout Items'

class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=50,
        choices=UserRoles.choices,
        default=UserRoles.CAN_VIEW  # Default role can be changed as needed
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}" # or return self.email if you prefer

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



class Delivery(models.Model):
    STATUS_CHOICES = [
        ('noc', 'NOC'),
        ('netdev', 'NetDev'),
        ('bolt', 'BOLT'),
        ('dci', 'DCI'),
        ('data_centre_infrastructure', 'Data Centre Infrastructure'),
        
    ]
    
    supplier_name = models.ForeignKey(Suppliers, on_delete=models.CASCADE, related_name='primary_suppliers', blank=True, null=True)
    quantity = models.PositiveIntegerField()
    date_delivered = models.DateField(auto_now_add=True)
    person_receiving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who received the asset")
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    invoice_number = models.CharField(max_length=100,null=True,blank=True)
    project = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default='noc',
        blank=True,
        null=True
    )
    comments = models.TextField(blank=True)
    delivery_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)  # SLK ID field
    
    @property
    def semantic_autocomplete(self):
        html = self.invoice_file()
        return format_html(html)


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
        return f'Consignment {self.delivery_id} from {self.supplier_name} on {self.date_delivered}'

    class Meta:
        verbose_name = 'Received Consignment'
        verbose_name_plural = 'Received Consignments'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
            verbose_name = 'Category'
            verbose_name_plural = 'Categories'

from django.db import models, transaction
from django.db.models import Max
import logging

logger = logging.getLogger(__name__)

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    name_alias = models.CharField(max_length=100, unique=True)
    location_code = models.CharField(max_length=10,unique=True,  editable=False, blank=True)  # KLC ID field

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        # Generate a unique KLC ID if not already set
        if not self.location_code:
            with transaction.atomic():
                # Fetch the maximum value of location_code
                last_code = Location.objects.aggregate(Max('location_code'))['location_code__max']
                if last_code:
                    try:
                        # Extract the integer part (e.g., from "KLC001" to 1)
                        last_id = int(last_code[3:])
                        new_id = last_id + 1
                    except ValueError:
                        logger.error(f"Invalid location_code format: {last_code}")
                        new_id = 1
                else:
                    new_id = 1

                # Format as KLC ID (e.g., "KLC001")
                self.location_code = f'KLC{new_id:03d}'
                logger.info(f"Generated location_code: {self.location_code}")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'



class Assets(models.Model):
    STATUS_CHOICES = [
        ('instore', 'In Store'),
        ('faulty', 'Faulty'),
        ('onsite', 'On Site'),
        ('decommissioned', 'Decommissioned'),
        ('pending_release', 'Pending Release'),
        ('pending_approval', 'Pending Approval '),
        ('approved', 'Approved by Admin '),
        ('rejected', 'Denied by Admin '),
    ]

    date_received = models.DateField(auto_now_add=True)
    person_receiving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text="User who received the asset")
    asset_description = models.TextField()
    asset_description_model = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    kenet_tag = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='primary_location', blank=True, null=True)
    sent_to_erp = models.BooleanField(default=False)
    destination_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='going_location', blank=True, null=True)
    asset_id = models.CharField(max_length=10, unique=True, editable=False, blank=True)  # ALK ID field
    
    
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
        return f"{self.asset_description} ({self.serial_number}) ({self.kenet_tag}) ({self.location}) ({self.asset_description_model}) ({self.status}) ({self.id}) ({self.destination_location})"

    def save(self, *args, **kwargs):
            # Generate a unique SLK ID if not already set
            if not self.asset_id:
                # Fetch the last created Delivery instance
                last_delivery = Assets.objects.all().order_by('id').last()
                if last_delivery:
                    last_id = int(last_delivery.asset_id[3:])  # Extract the integer part
                    new_id = last_id + 1
                else:
                    new_id = 1
                # Format as SLK ID (e.g., "SLK001")
                self.asset_id = f'ALK{new_id:03d}'
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['-id']
            


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.asset.serial_number}- {self.asset.status}- {self.asset.kenet_tag}- {self.asset.location}- {self.asset.id}- {self.asset.destination_location}- {self.added_at}"

    class Meta:
        unique_together = ('user', 'asset')  # Ensures an asset can only be in a user's cart once
        
    
    class Meta:
        verbose_name = 'Dispatch Basket'
        verbose_name_plural = 'Dispatch Baskets'
        # ordering = ['-date_created']  # Orders by most recent movements first

import base64
from django.core.files.base import ContentFile

def get_base64_image(image_field):
    if image_field:
        with open(image_field.path, 'rb') as img:
            return base64.b64encode(img.read()).decode('utf-8')
    return None


class Checkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField('Cart', related_name='checkouts')
    checkout_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    
    signature_image = models.ImageField(upload_to='signatures/', null=True, blank=True)
    user_signature_image = models.ImageField(upload_to='signatures/users/', null=True, blank=True)
    quantity_required = models.PositiveIntegerField(default=1)
    quantity_issued = models.PositiveIntegerField(default=1)
    # verifier_user = models.CharField(max_length=255, null=True, blank=True,)
    verifier_user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='verifier_user', on_delete=models.CASCADE,null=True,blank=True)
    checkout_url_link = models.URLField(blank=True, null=True, help_text="Optional URL for checkout link")
    
    pdf_file = models.FileField(upload_to='release_forms/', blank=True, null=True)

    def __str__(self):
        return f"Dispatched by {self.user.username} on {self.checkout_date}"

    def save_signature(self, signature_base64):
        try:
            if ',' in signature_base64:
                header, data = signature_base64.split(',')
            else:
                data = signature_base64
            decoded_file = base64.b64decode(data)
            self.signature_image.save('signature.png', ContentFile(decoded_file), save=False)
        except Exception as e:
            raise ValidationError(f"Failed to save signature: {e}")
        
    def save_user_signature(self, signature_base64):
        try:
            if ',' in signature_base64:
                header, data = signature_base64.split(',')
            else:
                data = signature_base64
            decoded_file = base64.b64decode(data)
            self.user_signature_image.save('user_signature.png', ContentFile(decoded_file), save=False)
        except Exception as e:
            raise ValidationError(f"Failed to save signature: {e}")

    def get_user_signature_url(self):
        if self.user_signature_image and hasattr(self.user_signature_image, 'url'):
            return self.user_signature_image.url
        return '/static/default_signature.png'  # Fallback image URL if no signature is found
    
    def get_signature_image_url(self):
        if self.signature_image and hasattr(self.signature_image, 'url'):
            return self.signature_image.url
        return '/static/default_signature.png'  # Fallback image URL if no signature is found

    
    def get_user_signature_base64(self):
        return get_base64_image(self.user_signature_image)

    def get_signature_base64(self):
        return get_base64_image(self.signature_image)

    def update_quantities(self, quantity_required: int, quantity_issued: int):
        if quantity_issued > quantity_required:
            raise ValidationError("Quantity issued cannot exceed quantity required.")
        self.quantity_required = quantity_required
        self.quantity_issued = quantity_issued
        self.save()

    def add_remarks(self, remarks: str):
        self.remarks = remarks
        self.save()

    def validate_authorizing_name(self):
        if not self.authorizing_name:
            raise ValidationError("Authorizing name cannot be empty.")

    class Meta:
        verbose_name = 'Dispatch List'
        verbose_name_plural = 'Dispatch Lists'
        ordering = ['-checkout_date']


class AssetsMovement(models.Model):
    assets = models.ForeignKey(Assets, on_delete=models.CASCADE, related_name='movements', help_text="Asset being moved")
    date_created = models.DateTimeField(auto_now_add=True, help_text="Date when the movement was recorded")
    person_moving = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, help_text="Person responsible for moving the asset")
    comments = models.TextField(blank=True, null=True, help_text="Additional details about the movement")
    asset_description = models.TextField(blank=True, null=True, help_text="Additional details about the asset")
    asset_description_model = models.TextField(blank=True, null=True, help_text="Additional details about the asset")
    serial_number = models.CharField(max_length=100, blank=True, null=True, help_text="The serial number of the asset")
    kenet_tag = models.CharField(max_length=100, blank=True, null=True, help_text="The KENET tag number of the asset")
    status = models.CharField(max_length=120, blank=True, null=True, help_text="Current status of the asset during the movement")
    location = models.CharField(max_length=200, blank=True, null=True, help_text="Current location of the asset")
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='primary_location', blank=True, null=True)
    new_location = models.CharField(max_length=200, blank=True, null=True, help_text="New location of the asset after movement")
    sent_to_erp = models.BooleanField(default=False)

    def __str__(self):
        return f"Movement of asset {self.assets.serial_number} recorded on {self.date_created} destination {self.new_location}"

    class Meta:
        verbose_name = 'Asset Movement'
        verbose_name_plural = 'Asset Movements'
        ordering = ['-date_created']  # Orders by most recent movements first




class SavedPDF(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PDF by {self.user.username} on {self.created_at}"


