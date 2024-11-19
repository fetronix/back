from django.apps import AppConfig

class KENETAssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'KENETAssets'

    def ready(self):
        # Import the task here, but don't execute it yet
        from KENETAssets.tasks import remove_expired_cart_items, process_rejected_cart_items
