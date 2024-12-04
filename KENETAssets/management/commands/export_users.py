from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Exports the custom User model data into a text file'

    def handle(self, *args, **kwargs):
        # Get the custom User model
        User = get_user_model()

        # File path for the exported data
        file_path = 'media/users.txt'

        # Fetch all users
        users = User.objects.all()

        # Write data to a text file
        with open(file_path, 'w') as file:
            for user in users:
                # Adjust fields based on your custom User model
                file.write(f"{user.id}\t{user.username}\t{user.email}\t{user.first_name}\t{user.last_name}\n")

        self.stdout.write(self.style.SUCCESS(f'Successfully exported users to {file_path}'))
