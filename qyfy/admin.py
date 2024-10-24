from django.contrib import admin
from .models import *

class AssetsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('asset_description','category','person_receiving', 'serial_number', 'kenet_tag', 'location', 'status', 'date_received','new_location')
    
    # Fields to search for in the admin interface
    search_fields = ('serial_number', 'kenet_tag', 'asset_description', 'location')
    
    # Fields that can be edited directly from the list view
    list_editable = ('status',)

    # Filters to filter the data by status or date received
    list_filter = ('status', 'date_received')

# Register the Assets model with the custom admin class
admin.site.register(Assets, AssetsAdmin)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Delivery)
admin.site.register(Cart)
@admin.register(ReleaseFormData)
class ReleaseFormDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'current_location', 'new_location', 'description', 'quantity_required', 'quantity_issued', 'created_at')
    list_filter = ('date', 'authorization_date', 'created_at')
    search_fields = ('name', 'serial_number', 'kenet_tag', 'authorizing_name')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Ensure this points to your CustomUser model

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
