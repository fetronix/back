from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import Cart, Checkout, Assets

# Task 1: Remove expired cart items with 'pending_release' status
@background(schedule=10)  # You can adjust the schedule time based on your needs
def remove_expired_cart_items():
    expiration_time = timezone.now() - timedelta(seconds=30)
    
    expired_cart_items = Cart.objects.filter(asset__status='pending_release', added_at__lt=expiration_time)
    
    for cart_item in expired_cart_items:
        # Update asset status to 'instore' before deleting from the cart
        asset = cart_item.asset
        asset.status = 'instore'
        asset.save()

        # Delete the cart item
        cart_item.delete()

        print(f"Removed expired cart item: {asset.serial_number} for user: {cart_item.user.username}")

# Task 2: Process rejected assets, revert status, and remove from checkout
@background(schedule=10)  # Adjust the schedule as needed
def process_rejected_cart_items():
    rejected_checkouts = Checkout.objects.filter(cart_items__asset__status='rejected')

    for checkout in rejected_checkouts:
        cart_items = checkout.cart_items.all()

        for cart_item in cart_items:
            asset = cart_item.asset
            asset.new_location = None
            asset.status = 'instore'
            asset.save()

            # Remove the cart item
            cart_item.delete()
            print(f"Processed rejected cart item: {asset.serial_number}")

        # Delete checkout if no remaining cart items
        if checkout.cart_items.count() == 0:
            checkout.delete()

    print("Rejected cart items have been processed and deleted.")
