from django.apps import AppConfig



class KENETAssetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'KENETAssets'
    
    def ready(self):
        import KENETAssets.tasks 
    
    
