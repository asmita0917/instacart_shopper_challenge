from django.core.management.base import BaseCommand
from shopper.models import Applicant

class Command(BaseCommand):
    args = 'number_of_entries'
    help = ''

    def _create_db(self, number_of_entries):
        print "requested number of entries %d" % number_of_entries
        applicant = Applicant(name='asmita', email='a@b.com', city='Santa Clara', state='CA')
        applicant.save()
        applicant = Applicant.objects.filter(email='a@b.com')
        print applicant[0].name
        print applicant[0].city

    def add_arguments(self, parser):
        parser.add_argument('number_of_entries', default=1000, nargs='?', type=int)
    
    def handle(self, *args, **options):
        number_of_entries = options['number_of_entries']
        self._create_db(number_of_entries)