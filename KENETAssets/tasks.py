from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import Cart, Checkout, Assets

# Task 1: Remove expired cart items with 'pending_release' status
@background(schedule=60)  # Default schedule to check periodically, e.g., every minute
def remove_expired_cart_items():
    # Get the current time and the next midnight
    now = timezone.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate expiration time (for items added before today)
    expiration_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Query for expired cart items
    expired_cart_items = Cart.objects.filter(
        asset__status='pending_release',
        added_at__lt=expiration_time
    )
    
    for cart_item in expired_cart_items:
        # Update asset status to 'instore' before deleting from the cart
        asset = cart_item.asset
        asset.status = 'instore'
        asset.save()

        # Delete the cart item
        cart_item.delete()

        print(f"Removed expired cart item: {asset.serial_number} for user: {cart_item.user.username}")

    print(f"Scheduled next run for: {midnight}")


# Task 2: Process rejected assets, revert status, and remove from checkout
@background(schedule=10)  # Adjust the schedule as needed
def process_rejected_cart_items():
    rejected_checkouts = Checkout.objects.filter(cart_items__asset__status='rejected')

    for checkout in rejected_checkouts:
        cart_items = checkout.cart_items.all()

        for cart_item in cart_items:
            asset = cart_item.asset
            asset.destination_location = None
            asset.status = 'instore'
            asset.save()

            # Remove the cart item
            cart_item.delete()
            print(f"Processed rejected cart item: {asset.serial_number}")

        # Delete checkout if no remaining cart items
        if checkout.cart_items.count() == 0:
            checkout.delete()

    print("Rejected cart items have been processed and deleted.")
