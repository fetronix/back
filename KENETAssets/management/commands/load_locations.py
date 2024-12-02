import pandas as pd
from django.core.management.base import BaseCommand
from KENETAssets.models import Location  # Adjust the import to your app name

class Command(BaseCommand):
    help = "Load locations from FA_Cleaned_Final.xlsx"

    def handle(self, *args, **kwargs):
        # Load the Excel file
        file_path = "media/FA_Cleaned_Final.xlsx"  # Replace with the actual path
        data = pd.read_excel(file_path)

        # Iterate through the data and save it to the database
        for _, row in data.iterrows():
            name = row.get('Name')  # Adjust column name to match the Excel header
            name_alias = row.get('Code')  # Adjust column name to match the Excel header

            if name and name_alias:  # Ensure no empty entries
                location, created = Location.objects.get_or_create(
                    name=name,
                    name_alias=name_alias
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {name} ({name_alias})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped: {name} ({name_alias}) - Already exists"))

        self.stdout.write(self.style.SUCCESS("Import completed!"))
