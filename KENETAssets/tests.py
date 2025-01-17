from django.test import TestCase
from .models import Location, Assets

# class LocationModelTest(TestCase):
#     def test_location_creation(self):
#         location = Location.objects.create(name="Test Location")
#         self.assertEqual(location.name, "Test Location")
#         self.assertIsNotNone(location.id)  # Ensure that an ID was assigned

#     def test_location_generate_unique_id(self):
#         location = Location(name="New Location")
#         # Test that the unique ID generation logic works
#         location.save()
#         self.assertEqual(location.id, 1)

# from django.test import TestCase
# from django.core.exceptions import ValidationError
# from .models import CustomUser, UserRoles

# class CustomUserTestCase(TestCase):
#     def test_create_user_with_valid_email(self):
#         user = CustomUser.objects.create_user(username='john_doe', email='john.doe@kenet.or.ke', password='testpassword')
#         self.assertEqual(user.email, 'john.doe@kenet.or.ke')

#     def test_create_user_with_invalid_email(self):
#         with self.assertRaises(ValidationError):
#             user = CustomUser.objects.create_user(username='john_doe', email='john.doe@gmail.com', password='testpassword')

#     def test_user_role(self):
#         user = CustomUser.objects.create_user(username='john_doe', email='john.doe@kenet.or.ke', password='testpassword', role=UserRoles.CAN_VERIFY_ITEMS)
#         self.assertEqual(user.role, UserRoles.CAN_VERIFY_ITEMS)


# from django.test import TestCase
# from .models import Suppliers

# class SuppliersTestCase(TestCase):
#     def test_create_supplier(self):
#         supplier = Suppliers.objects.create(name="ABC Supplies")
#         self.assertEqual(supplier.name, "ABC Supplies")
    
#     def test_duplicate_supplier(self):
#         Suppliers.objects.create(name="ABC Supplies")
#         with self.assertRaises(Exception):  # Assuming a unique constraint
            # Suppliers.objects.create(supplier_name="ABC Supplies")
            
            
# from django.test import TestCase
# from .models import Delivery, Suppliers, CustomUser

# class DeliveryTestCase(TestCase):
#     def setUp(self):
#         self.supplier = Suppliers.objects.create(name="ABC Supplies")
#         self.user = CustomUser.objects.create_user(username="john_doe", email="john.doe@kenet.or.ke", password="password")

#     def test_create_delivery(self):
#         delivery = Delivery.objects.create(
#             supplier_name=self.supplier,
#             quantity=10,
#             person_receiving=self.user,
#             invoice_number="INV1234",
#             project="noc"
#         )
#         self.assertEqual(delivery.supplier_name.name, "ABC Supplies")
#         self.assertEqual(delivery.quantity, 10)

#     def test_generate_delivery_id(self):
#         delivery = Delivery.objects.create(
#             supplier_name=self.supplier,
#             quantity=5,
#             person_receiving=self.user,
#             invoice_number="INV1234",
#             project="noc"
#         )
#         self.assertTrue(delivery.delivery_id.startswith("SLK"))


# from django.test import TestCase
# from .models import Location

# class LocationTestCase(TestCase):
#     def test_create_location(self):
#         location = Location.objects.create(name="Location A", name_alias="LocA")
#         self.assertEqual(location.name, "Location A")

#     def test_location_code_format(self):
#         location = Location.objects.create(name="Location B", name_alias="LocB")
#         self.assertTrue(location.location_code.startswith("KLC"))

# from django.test import TestCase
# from .models import Assets, Location, CustomUser, Category, Delivery,Suppliers

# class AssetsTestCase(TestCase):
#     def setUp(self):
#         # Ensure that 'name_alias' values are unique in the test
#         self.location = Location.objects.create(name="Location A", name_alias="LocA")
#         self.supplier_name = Suppliers.objects.create(name="Supplier A")  # Unique 'name_alias'
        
#         # Create a user for the asset receiving process
#         self.user = CustomUser.objects.create_user(username="john_doe", email="john.doe@kenet.or.ke", password="password")
        
#         # Create a category for the asset
#         self.category = Category.objects.create(name="Hardware")
        
#         # Create a delivery record for the asset
#         self.delivery = Delivery.objects.create(
#             supplier_name=self.supplier_name,
#             quantity=10,
#             person_receiving=self.user,
#             invoice_number="INV1234",
#             project="noc"
#         )

#     def test_create_asset(self):
#         # Create an asset and check if the asset fields are correct
#         asset = Assets.objects.create(
#             asset_description="New Asset",
#             serial_number="SN12345",
#             kenet_tag="KENET001",
#             location=self.location,
#             status="instore",
#             category=self.category,
#             delivery=self.delivery
#         )
#         self.assertEqual(asset.asset_description, "New Asset")
#         self.assertEqual(asset.serial_number, "SN12345")

#     def test_generate_asset_id(self):
#         # Create an asset and check if the asset ID starts with "ALK"
#         asset = Assets.objects.create(
#             asset_description="New Asset",
#             serial_number="SN12345",
#             kenet_tag="KENET001",
#             location=self.location,
#             status="instore",
#             category=self.category,
#             delivery=self.delivery
#         )
#         self.assertTrue(asset.asset_id.startswith("ALK"))

from django.test import TestCase
from .models import Cart, Assets, CustomUser

class CartTestCase(TestCase):
    def setUp(self):
        # Set up initial data for testing
        self.user = CustomUser.objects.create_user(username="john_doe", email="john.doe@kenet.or.ke", password="password")
        self.asset = Assets.objects.create(
            asset_description="Asset in Cart",
            serial_number="SN12345",
            kenet_tag="KENET001",
            status="instore"
        )

    def test_add_to_cart(self):
        # Test adding an asset to the cart
        cart = Cart.objects.create(user=self.user, asset=self.asset)
        self.assertEqual(cart.user.username, "john_doe")
        self.assertEqual(cart.asset.serial_number, "SN12345")

    def test_unique_cart_item(self):
        # Test unique constraint - should raise an exception when adding the same asset twice to the same user's cart
        Cart.objects.create(user=self.user, asset=self.asset)
        
        # Try adding the same asset again
        with self.assertRaises(Exception):  # Unique constraint violation
            Cart.objects.create(user=self.user, asset=self.asset)
