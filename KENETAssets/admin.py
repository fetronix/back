from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin
class AssetsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('asset_description','category','person_receiving', 'serial_number', 'kenet_tag', 'location','new_location', 'status', 'date_received')
    
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
admin.site.register(Checkout)
admin.site.register(AssetsMovement)
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

