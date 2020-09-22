from django.core.management.base import BaseCommand
from persons.models import Person

class Command(BaseCommand):
    persons = Person.objects.all()

    def handle(self, *args, **options):
        for person in self.persons:
            person.delete()