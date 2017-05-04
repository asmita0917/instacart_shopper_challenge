from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = '<Foobar>'
    help = ''

    def handle(self, *args, **options):
        print "Working"