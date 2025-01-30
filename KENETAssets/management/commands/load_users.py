from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Loads users from a text file into the User model'

    def handle(self, *args, **kwargs):
        file_path = 'media/users.txt'  # Path to your data file

        User = get_user_model()

        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            # Split the line into fields (assuming tab-separated)
            fields = line.strip().split('\t')
            if len(fields) == 4:
                user_id, username,first_name,last_name, email, password = fields

                # Create or update the user
                User.objects.update_or_create(
                    id=user_id,
                    defaults={
                        'username': username,
                        'email': email,
                        'first_name':first_name,
                        'last_name':last_name,
                        'is_active': True,
                    }
                )
                # Set the password
                user = User.objects.get(id=user_id)
                user.set_password(password)
                user.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded users into the database!'))
