import json
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand

from persons.models import Person

class Command(BaseCommand):
    """
    Imports all persons from the export.json file. 
    Database must be empty or all ids in the export.json file must be unused.
    """
    root = Path(__file__).parent.resolve()
    filename = Path(root, "export.json")
    persons_objects = []

    def convert_string_to_date(self, date):
        return datetime.strptime(date, '%Y-%m-%d').date()

    def create_person_object(self, person):
        return Person(
            pk=person["id"],
            first_name=person["first_name"],
            last_name=person["last_name"],
            maiden_name=person["maiden_name"],
            gender=person["gender"],
            date_of_birth=person["date_of_birth"],
            date_of_death=person["date_of_death"],
            mother=None,
            father=None,
            hometown=person["hometown"],
            infos=person["infos"]
        )

    def handle(self, *args, **options):
        with open(self.filename, "r") as fp:
            persons = json.load(fp)

        # creates all persons without setting the foreign key. 
        for person in persons:
            if person["date_of_birth"]:
                person["date_of_birth"] = self.convert_string_to_date(person["date_of_birth"])
            if person["date_of_death"]:
                person["date_of_death"] = self.convert_string_to_date(person["date_of_death"])
            self.persons_objects.append(self.create_person_object(person))
            
        Person.objects.bulk_create(self.persons_objects)

        #connects all persons to their mother or father
        for person in persons:
            if person["mother_id"]:
                p = Person.objects.get(pk=person["id"])
                mother = Person.objects.get(pk=person["mother_id"])
                p.mother = mother
                p.save()
            if person["father_id"]:
                p = Person.objects.get(pk=person["id"])
                father = Person.objects.get(pk=person["father_id"])
                p.father = father
                p.save()