from django.conf import settings
from django.contrib import admin
from .models import AppVersion

class AppVersionAdmin(admin.ModelAdmin):
    list_display = ['version', 'apk_file', 'update_url']
    search_fields = ['version']
    readonly_fields = ['update_url']  # Make the update URL read-only

    def save_model(self, request, obj, form, change):
        # When the model is saved, automatically update the update_url
        if obj.apk_file:
            obj.update_url = f"{settings.MEDIA_URL}apps/{obj.apk_file.name}"
        super().save_model(request, obj, form, change)

admin.site.register(AppVersion, AppVersionAdmin)
