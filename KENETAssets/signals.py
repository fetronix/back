# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .tasks import remove_expired_cart_items

@receiver(post_migrate)
def schedule_task(sender, **kwargs):
    # Schedule the task after the app is ready
    remove_expired_cart_items(repeat=10)
