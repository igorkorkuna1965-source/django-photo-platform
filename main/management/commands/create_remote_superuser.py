from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create or update superuser on remote server'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'Ihor5'
        password = 'Ihor12345'
        email = ''

        user, created = User.objects.get_or_create(username=username, defaults={"email": email})

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Password for {username} updated'))