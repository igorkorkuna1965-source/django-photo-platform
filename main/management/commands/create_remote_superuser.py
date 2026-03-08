from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create or update superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = "Ihor5"
        password = "Ihor12345"
        email = ""

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email}
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS("Superuser password reset"))