import pandas as pd
from django.core.management.base import BaseCommand
from KENETAssets.models import Assets, Location, CustomUser, Category, Delivery

class Command(BaseCommand):
    help = "Import assets from an Excel file"

    def handle(self, *args, **kwargs):
        # Path to the Excel file
        file_path = "media/testAsset.xlsx"
        
        # Load the Excel file
        df = pd.read_excel(file_path)
        
        for _, row in df.iterrows():
            try:
                # Fetch foreign key relationships
                location = Location.objects.filter(id=row['Location']).first()
                category = Category.objects.filter(id=row['Category']).first()
                delivery = Delivery.objects.filter(id=row['delivery']).first()

                # Fetch the person receiving based on email
                person = CustomUser.objects.filter(email=row['Person Receiving']).first()
                if not person:
                    self.stdout.write(self.style.WARNING(f"Person Receiving '{row['Person Receiving']}' not found. Skipping asset."))
                    continue

                # Check for duplicates
                existing_asset = Assets.objects.filter(serial_number=row['Serial Number']).first()
                if existing_asset:
                    self.stdout.write(self.style.WARNING(f"Asset with Serial Number '{row['Serial Number']}' already exists. Skipping."))
                    continue

                # Create the asset
                asset = Assets.objects.create(
                    asset_description=row['Asset Description'],
                    asset_description_model=row['Asset Description Model'],
                    serial_number=row['Serial Number'],
                    kenet_tag=row['KENET Tag Number'],
                    location=location,
                    person_receiving=person,
                    category=category,
                    delivery=delivery,
                    status=row['status'],
                )
                asset.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully imported asset: {asset.serial_number}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing asset {row['Serial Number']}: {str(e)}"))
