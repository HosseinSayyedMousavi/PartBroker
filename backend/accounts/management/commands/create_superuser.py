
from django.core.management.base import BaseCommand
from accounts.models import User
from decouple import config
class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(phone_number="09339496041").exists():
            User.objects.create_superuser("09339496041","123")
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
