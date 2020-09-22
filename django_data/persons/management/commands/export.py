from django.core.management.base import BaseCommand
from persons.models import Person
from pathlib import Path
import json

class Command(BaseCommand):
    root = Path(__file__).parent.resolve()
    filename = Path(root, "export.json")
    persons = list(Person.objects.all().values())

    def convert_date_to_string(self, date):
        return date.strftime("%Y-%m-%d")


    def handle(self, *args, **options):
        for person in self.persons:
            if person["date_of_birth"]:
                person["date_of_birth"] = self.convert_date_to_string(person["date_of_birth"])
            if person["date_of_death"]:
                person["date_of_death"] = self.convert_date_to_string(person["date_of_death"])

        with open(self.filename, "w") as fp:
            json.dump(self.persons, fp)