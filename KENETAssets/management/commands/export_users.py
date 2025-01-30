# locations/management/commands/export_locations_to_xlsx.py
import openpyxl
from django.core.management.base import BaseCommand
from KENETAssets.models import Location

class Command(BaseCommand):
    help = 'Exports all locations with their ID numbers to an Excel file'

    def handle(self, *args, **kwargs):
        # Fetch all locations from the database
        locations = Location.objects.all()

        # Create a new workbook and active sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Locations'

        # Add the headers to the first row
        sheet['A1'] = 'ID'
        sheet['B1'] = 'Location Code'
        sheet['C1'] = 'Name'
        sheet['D1'] = 'Name Alias'

        # Populate the rows with location data
        row = 2  # Start from the second row
        for location in locations:
            sheet[f'A{row}'] = location.id
            sheet[f'B{row}'] = location.location_code
            sheet[f'C{row}'] = location.name
            sheet[f'D{row}'] = location.name_alias
            row += 1

        # Save the workbook to a file
        filename = 'locations.xlsx'
        workbook.save(filename)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported locations to {filename}'))
