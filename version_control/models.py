from django.conf import settings
from django.db import models

class AppVersion(models.Model):
    version = models.CharField(max_length=50)
    update_url = models.URLField()
    apk_file = models.FileField(upload_to='apps/', null=True, blank=True)  # This will store the uploaded APK file

    def __str__(self):
        return self.version
    
    def save(self, *args, **kwargs):
        # Automatically generate the update_url after file upload
        if self.apk_file:
            self.update_url = f"http://197.136.16.164:8000{settings.MEDIA_URL}apps/{self.apk_file.name}"
        super().save(*args, **kwargs)
