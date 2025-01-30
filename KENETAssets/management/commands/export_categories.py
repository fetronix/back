from django.core.management.base import BaseCommand
from KENETAssets.models import Category

class Command(BaseCommand):
    help = 'Exports the Category model data into a text file'

    def handle(self, *args, **kwargs):
        # File path for the exported data
        file_path = 'media/categories.txt'

        # Fetch all categories
        categories = Category.objects.all()

        # Write data to a text file
        with open(file_path, 'w') as file:
            for category in categories:
                file.write(f"{category.id}\t{category.name}\n")

        self.stdout.write(self.style.SUCCESS(f'Successfully exported categories to {file_path}'))
