from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import Cart
from background_task import background
from django.utils import timezone
from datetime import timedelta
from .models import Cart, Checkout, Assets
from django.db import transaction


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

@background(schedule=10)  # 10-second delay for the task
def process_rejected_cart_items():
    # Get all checkout items with rejected assets
    rejected_checkouts = Checkout.objects.filter(cart_items__asset__status='rejected')

    for checkout in rejected_checkouts:
        # For each rejected checkout, get the related cart items
        cart_items = checkout.cart_items.all()

        for cart_item in cart_items:
            # Get the asset linked to the cart item
            asset = cart_item.asset

            # Revert asset's new_location to null and status to 'instore'
            asset.new_location = None
            asset.status = 'instore'

            # Save the asset
            asset.save()

            # Now delete the cart item
            cart_item.delete()

            # Optionally, print for debugging
            print(f"Rejected cart item processed: {asset.serial_number}")

        # After processing all cart items, check if checkout has any cart items left
        if checkout.cart_items.count() == 0:
            # Only delete the checkout if there are no remaining cart items
            checkout.delete()

    print("Rejected cart items have been processed and deleted.")
