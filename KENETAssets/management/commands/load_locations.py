# locations/management/commands/load_locations.py
from django.core.management.base import BaseCommand
from KENETAssets.models import Location

class Command(BaseCommand):
    help = 'Loads locations from a text file into the Locations table'

    def handle(self, *args, **kwargs):
        # Path to your text file
        file_path = 'media/kenya_locations.txt'

        # Open the file and read lines
        with open(file_path, 'r') as file:
            locations = file.readlines()

        # Add each location to the database
        for location in locations:
            location = location.strip()  # Remove any extra whitespace or newlines
            if location:
                Location.objects.create(name=location)

        self.stdout.write(self.style.SUCCESS('Successfully loaded locations into the database!'))
