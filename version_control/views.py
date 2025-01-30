from django.http import JsonResponse
from .models import AppVersion  # Ensure this import is correct

def get_latest_version(request):
    # Get the latest version from the database
    version = AppVersion.objects.first()  # Assumes only one record in the DB for simplicity

    # If no version found in the database, return a fallback version
    if version:
        response_data = {
            'latest_version': version.version,
            'update_url': version.update_url
        }
    else:
        # Return default version details if no version exists in DB
        response_data = {
            'latest_version': '1.0.0',  # Default version if no entry in DB
            'update_url': 'http://197.136.16.133/assets-apk/app-release.apk'  # Fallback URL
        }

    # Return the JSON response
    return JsonResponse(response_data)
