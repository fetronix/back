from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.html import format_html
from .models import AssetsMovement
from django.contrib import admin
from .models import AssetsMovement
from django.urls import reverse

from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect

class AssetsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('asset_id','asset_description', 'asset_description_model', 'category', 'person_receiving', 
                    'serial_number', 'kenet_tag', 'location', 'status', 'date_received', 'custom_action')
    
    # Fields to search for in the admin interface
    search_fields = ('serial_number', 'kenet_tag', 'asset_description', 'location')
    
    # Filters to filter the data by status or date received
    list_filter = ('status', 'date_received')

    def custom_action(self, obj):
        # If the asset has already been sent to ERP, show a green button with a new label
        if obj.sent_to_erp:
            return format_html(
                '<button class="ui green button" type="button" disabled>Data Sent to ERP</button>'
            )
        else:
            # Otherwise, show the normal "Send to ERP" button
            url = reverse('create_fixed_asset', args=[obj.pk])  # URL for the ERP creation view
            return format_html(
                '<a href="{0}" class="ui blue button" type="button">Send to E.R.P</a>',
                url
            )

    custom_action.short_description = 'Send to E.R.P'
    custom_action.allow_tags = True

    # Override the save model to update `sent_to_erp` field after sending data to ERP
    def save_model(self, request, obj, form, change):
        if change and 'sent_to_erp' not in form.changed_data:  # Only update if the object is saved
            if obj.sent_to_erp:  # Check if the status is already sent to ERP
                # Optional: Add your logic to update or trigger your ERP-related functionality here.
                pass
        super().save_model(request, obj, form, change)
    
# Register the admin class
admin.site.register(Assets, AssetsAdmin)

admin.site.register(Category)
admin.site.register(SavedPDF)
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    # Display 'name' and 'name_alias' in the list view
    list_display = ('name', 'name_alias','location_code')

    # Add search functionality for 'name' and 'name_alias'
    search_fields = ('name', 'name_alias','location_code')

    # If you want to filter by other fields, add them to 'list_filter'
    # (Assumes there are fields like 'created_at' or other categorical fields)
    list_filter = ('name', 'name_alias','location_code')
    
    # Set default ordering alphabetically by 'name' (A to Z)
    ordering = ('name',)  # Add '-name' for Z to A ordering
    
    # def custom_action(self, obj):
    #     # If the asset has already been sent to ERP, show a green button with a new label
    #     if obj.sent_to_erp:
    #         return format_html(
    #             '<button class="ui green button" type="button" disabled>Location Sent to ERP</button>'
    #         )
    #     else:
    #         # Otherwise, show the normal "Send to ERP" button
    #         url = reverse('create_fixed_asset', args=[obj.pk])  # URL for the ERP creation view
    #         return format_html(
    #             '<a href="{0}" class="ui blue button" type="button">Send to E.R.P</a>',
    #             url
    #         )

    # custom_action.short_description = 'Send to E.R.P'
    # custom_action.allow_tags = True

    # # Override the save model to update `sent_to_erp` field after sending data to ERP
    # def save_model(self, request, obj, form, change):
    #     if change and 'sent_to_erp' not in form.changed_data:  # Only update if the object is saved
    #         if obj.sent_to_erp:  # Check if the status is already sent to ERP
    #             # Optional: Add your logic to update or trigger your ERP-related functionality here.
    #             pass
    #     super().save_model(request, obj, form, change)
    
    
admin.site.register(Delivery)
admin.site.register(Cart)
class FibreInfrastructureAdmin(admin.ModelAdmin):
    list_display = (
        'location_code',
        'start_location',
        'intermediary_locations',
        'destination_location',
    )
    search_fields = (
        'location_code',
        'start_location',
        'destination_location',
        'intermediary_locations',
    )
    list_filter = (
        'start_location',
        'destination_location',
    )
    ordering = ('location_code',)

admin.site.register(FibreInfrastructure, FibreInfrastructureAdmin)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'checkout_date', 'quantity_required', 'quantity_issued', 'signature_image')
    list_filter = ('checkout_date',)
    search_fields = ('user__username', 'remarks',)
    readonly_fields = ('verifier_user',)

    def signature_image_preview(self, obj):
        if obj.signature_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;" />', obj.signature_image.url)
        return "No Image"

    signature_image_preview.short_description = "Signature Image"

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        # Remove 'verifier_user' from the fields if present
        return [field for field in fields if field != 'checkout_url_link']

admin.site.register(Checkout, CheckoutAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import AssetsMovement

class AssetsMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_description', 'asset_description_model','serial_number','person_moving', 'status', 'location', 'new_location', 'date_created', 'custom_action')
    list_filter = ('status', 'location', 'new_location', 'date_created')
    search_fields = ('assets__serial_number', 'assets__kenet_tag', 'person_moving__username', 'comments')

    # Disable add permission
    def has_add_permission(self, request):
        return False

    # Disable delete permission
    def has_delete_permission(self, request, obj=None):
        return False

    # Disable change permission
    def has_change_permission(self, request, obj=None):
        return False

    def custom_action(self, obj):
        # If the asset has already been sent to ERP, show a green button with a new label
        if obj.sent_to_erp:
            return format_html(
                '<button class="ui red button" type="button" disabled>Data Updated on ERP</button>'
            )
        else:
            # Otherwise, show the normal "Send to ERP" button
            url = reverse('update_fixed_asset', args=[obj.pk])  # URL for the ERP creation view
            return format_html(
                '<a href="{0}" class="ui blue button" type="button">Update on E.R.P</a>',
                url
            )

    custom_action.short_description = 'Update on E.R.P'
    custom_action.allow_tags = True

# Register the customized admin view
admin.site.register(AssetsMovement, AssetsMovementAdmin)



admin.site.register(Suppliers)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'role']  # Added role for filtering
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role', 'is_staff', 'is_active')}),
        ('Permissions', {'fields': ('is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

# Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)

