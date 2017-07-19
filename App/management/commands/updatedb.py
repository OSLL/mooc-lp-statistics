from django.core.management.base import BaseCommand
import App.another_functions

class Command(BaseCommand):
    help = 'Updating Database'

    def handle(self, *args, **options):
        App.another_functions.updateLogInDb()