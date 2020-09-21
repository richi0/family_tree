from django.db import models
from django.urls import reverse
from datetime import date


class Person(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    maiden_name = models.CharField(max_length=120, null=True, blank=True)
    M = "Male"
    F = "Female"
    GENDER_CHOICES = [(M, "Male"), (F, "Female")]
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default=M,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    mother = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name='child_m', null=True, blank=True)
    father = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name='child_f', null=True, blank=True)
    hometown = models.CharField(max_length=120)
    infos = models.TextField(null=True, blank=True)

    def __str__(self):
        if self.date_of_birth:
            return f"{self.first_name} {self.last_name} {self.date_of_birth.year}"
        else:
            return f"{self.first_name} {self.last_name}"

    def age(self):
        today = date.today()
        if (self.date_of_birth and self.date_of_death):
            return self.date_of_death.year-self.date_of_birth.year
        elif (self.date_of_birth):
            return today.year-self.date_of_birth.year
        else:
            return None

    def sort_by_date(self, key):
        if key:
            return key
        else:
            return date.today()

    def get_children(self):
        if self.child_m.all():
            child = self.child_m.all()
        elif self.child_f.all():
            child = self.child_f.all()
        else:
            return []
        return sorted(list(child), key=lambda child: self.sort_by_date(child.date_of_birth))

    def get_spouse(self):
        child = list(self.get_children())
        if child:
            if self.gender == "Male":
                return child[0].mother
            else:
                return child[0].father
        else:
            return False

    def get_siblings(self):
        if self.mother:
            return self.mother.get_children()
        elif self.father:
            return self.father.get_children()
        else:
            return False

    def get_detail_url(self):
        return reverse('person_detail', args=[str(self.id)])

    def get_absolute_url(self):
        return reverse('person_detail', args=[str(self.id)])

    def get_update_url(self):
        return reverse('person_update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('person_delete', args=[str(self.id)])
