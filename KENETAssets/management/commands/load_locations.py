# locations/management/commands/load_locations.py
from django.core.management.base import BaseCommand
from KENETAssets.models import Location

class Command(BaseCommand):
    help = 'Loads locations from a text file into the Locations table with name and name_alias fields'

    def handle(self, *args, **kwargs):
        # Path to your text file
        file_path = 'media/cleaned_updated_name_name_alias1.txt'

        # Open the file and read lines
        with open(file_path, 'r') as file:
            locations = file.readlines()

        # Add each location to the database
        for line in locations:
            # Split line into name and name_alias (assuming tab separation)
            fields = line.strip().split('\t')
            if len(fields) == 2:
                name, name_alias = fields
                # Create a Location instance with both name and name_alias
                Location.objects.create(name=name, name_alias=name_alias)

        self.stdout.write(self.style.SUCCESS('Successfully loaded locations into the database!'))
