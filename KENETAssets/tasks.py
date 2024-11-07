from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import Cart

@background(schedule=10)  # Run this task every 10 seconds
def remove_expired_cart_items():
    expiration_time = timezone.now() - timedelta(seconds=30)

    # Query all cart items with assets marked as pending_release and older than 30 seconds
    expired_cart_items = Cart.objects.filter(asset__status='pending_release', added_at__lt=expiration_time)

    # Loop through expired cart items and update asset status before deleting the cart item
    for cart_item in expired_cart_items:
        # Update the asset's status to 'instore'
        cart_item.asset.status = 'instore'
        cart_item.asset.save()  # Save the updated asset status

        # Now delete the cart item
        cart_item.delete()

        print(f"Removed cart item: {cart_item.asset.serial_number} for user: {cart_item.user.username}")
