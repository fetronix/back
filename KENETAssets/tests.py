from django.test import TestCase
from .models import Location, Assets

class LocationModelTest(TestCase):
    def test_location_creation(self):
        location = Location.objects.create(name="Test Location")
        self.assertEqual(location.name, "Test Location")
        self.assertIsNotNone(location.id)  # Ensure that an ID was assigned

    def test_location_generate_unique_id(self):
        location = Location(name="New Location")
        # Test that the unique ID generation logic works
        location.save()
        self.assertEqual(location.id, 1)
