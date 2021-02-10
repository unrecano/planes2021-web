from django.core.management.base import BaseCommand, CommandError
from planes import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'base directory: {settings.BASE_DIR}'))
        self.stdout.write(self.style.SUCCESS(f'debug: {settings.DEBUG}'))
        self.stdout.write(self.style.SUCCESS(f'allowed hosts: {settings.ALLOWED_HOSTS}'))