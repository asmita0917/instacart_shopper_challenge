from django.core.management.base import BaseCommand
from shopper.models import Applicant
from random import choice, randint
from string import ascii_lowercase
from django.db import IntegrityError
import time

class Command(BaseCommand):
    args = 'number_of_entries'
    help = ''

    # Use generators to possibly get unique names accross different calls
    def name_generator(self):
        while True:
            yield ''.join(choice(ascii_lowercase) for _ in xrange(randint(5, 10)))            

    def email_address_generator(self, name_gen):
        hosts=('gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com')
        while True:
            user_name = next(name_gen)
            yield '%s@%s' % (user_name,choice(hosts))
    
    def date_generator(self):
        # 01 Jan 2010 00:00:01 GMT
        start_time = 1262304001  
        # 31 Dec 2014 23:59 59 GMT
        end_time = 1420070399  
        time_int = randint(start_time, end_time)
        return time.strftime('%Y-%m-%d', time.localtime(time_int))

    def city_state_gen(self):
        cities=['San Francisco, CA', 'Santa Clara, CA', 'Seattle, WA', 'New York, NY', 'Atlanta, GA']
        return choice(cities).split(',')
    
    def workflow_state_gen(self):
        workflow_states=['applied', 'quiz_started', 'quiz_completed', 'onboarding_requested', 'onboarding_completed', 'hired', 'rejected']
        return choice(workflow_states)


    def _create_db(self, number_of_entries):
        name_gen = self.name_generator()
        email_gen = self.email_address_generator(name_gen)

        i = 0
        while i < number_of_entries: 
            first_name = next(name_gen)
            last_name = next(name_gen)
            email = next(email_gen)
            city_state = self.city_state_gen()
            city = city_state[0].strip()
            state = city_state[1].strip()
            application_date = self.date_generator()
            workflow_state = self.workflow_state_gen()
            applicant = Applicant(first_name=first_name, last_name=last_name, email=email, city=city, state=state, application_date=application_date, workflow_state=workflow_state)
            try:
                applicant.save()
            except IntegrityError:
                i = i - 1;
            i = i + 1;


    def add_arguments(self, parser):
        parser.add_argument('number_of_entries', default=1000, nargs='?', type=int)

    def handle(self, *args, **options):
        number_of_entries = options['number_of_entries']
        self._create_db(number_of_entries)
