from django.core.management.base import BaseCommand
from KENETAssets.models import Category

class Command(BaseCommand):
    help = 'Loads categories from a text file into the Category model'

    def handle(self, *args, **kwargs):
        file_path = 'media/categories.txt'  # Path to your data file

        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            # Split the line into fields (assuming tab-separated)
            fields = line.strip().split('\t')
            if len(fields) == 2:
                category_id, name = fields

                # Create or update the category
                Category.objects.update_or_create(
                    id=category_id,
                    defaults={'name': name}
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded categories into the database!'))
