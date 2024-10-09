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
