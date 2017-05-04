from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = 'number_of_entries'
    help = ''

    def _create_db(self, number_of_entries):
        print "requested number of entries %d" % number_of_entries

    def add_arguments(self, parser):
        parser.add_argument('number_of_entries', default=1000, nargs='?', type=int)
    
    def handle(self, *args, **options):
        number_of_entries = options['number_of_entries']
        self._create_db(number_of_entries)