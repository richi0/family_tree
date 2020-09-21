from django.test import TestCase
from django.urls import reverse, resolve

from .views import (PersonListView, PersonDetailView,
                    PersonCreateView, PersonUpdateView, PersonDeleteView)
from .models import Person


def create_person():
    return Person.objects.create(
        first_name="Ylmaz",
        last_name="Zett",
        maiden_name=None,
        gender="Male",
        date_of_birth="2005-03-03",
        date_of_death="2015-04-04",
        mother=None,
        father=None,
        hometown="Lucerne",
        infos="Best person alive!"
    )


class PersonTests(TestCase):
    def setUp(self):
        self.person = create_person()

    def test_person_listings(self):
        self.assertEqual(f"{self.person.first_name}", "Ylmaz")
        self.assertEqual(f"{self.person.last_name}", "Zett")
        self.assertEqual(self.person.maiden_name, None)
        self.assertEqual(f"{self.person.gender}", "Male")
        self.assertEqual(f"{self.person.date_of_birth}", "2005-03-03")
        self.assertEqual(f"{self.person.date_of_death}", "2015-04-04")
        self.assertEqual(self.person.mother, None)
        self.assertEqual(self.person.father, None)
        self.assertEqual(f"{self.person.hometown}", "Lucerne")
        self.assertEqual(f"{self.person.infos}", "Best person alive!")


class PersonListTests(TestCase):
    def setUp(self):
        url = reverse("person_list")
        self.response = self.client.get(url)

    def test_person_list_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_person_list_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "persons/person_list.html")

    def test_person_list_contains(self):
        self.assertContains(self.response, "Birthday")

    def test_person_list_contains_not(self):
        self.assertNotContains(self.response, "Hello")

    def test_person_list_resolves_personlistview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, PersonListView.as_view().__name__)


class PersonDetailTests(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(f"/person/{str(self.person.id)}/")
        self.no_response = self.client.get("/person/20/")

    def test_person_detail_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_person_detail_status_code_404(self):
        self.assertEqual(self.no_response.status_code, 404)

    def test_person_detail_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "persons/person_detail.html")

    def test_person_detail_contains(self):
        self.assertContains(self.response, "Ylmaz")
        self.assertContains(self.response, "Zett")
        self.assertContains(self.response, "Male")
        self.assertContains(self.response, "Lucerne")
        self.assertContains(self.response, "Best person alive!")

    def test_person_detail_contains_not(self):
        self.assertNotContains(self.response, "Married to")

    def test_person_detail_resolves_personupdateview(self):
        view = resolve(f'/person/{str(self.person.id)}/')
        self.assertEqual(view.func.__name__,
                         PersonDetailView.as_view().__name__)


class PersonUpdateTests(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(f"/person/{str(self.person.id)}/edit/")
        self.no_response = self.client.get("/person/20/edit/")

    def test_person_update_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_person_update_status_code_404(self):
        self.assertEqual(self.no_response.status_code, 404)

    def test_person_update_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "persons/person_update.html")

    def test_person_update_contains(self):
        self.assertContains(self.response, "Ylmaz")

    def test_person_update_contains_not(self):
        self.assertNotContains(self.response, "Bye")

    def test_person_update_resolves_personupdateview(self):
        view = resolve(f'/person/{str(self.person.id)}/edit/')
        self.assertEqual(view.func.__name__,
                         PersonUpdateView.as_view().__name__)


class PersonCreateTests(TestCase):
    def setUp(self):
        url = reverse("person_create")
        self.response = self.client.get(url)

    def test_person_create_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_person_create_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "persons/person_create.html")

    def test_person_create_contains(self):
        self.assertContains(self.response, "Create")

    def test_person_create_contains_not(self):
        self.assertNotContains(self.response, "Bye")

    def test_person_create_resolves_personcreateview(self):
        view = resolve('/person/new/')
        self.assertEqual(view.func.__name__,
                         PersonCreateView.as_view().__name__)


class PersonDeleteTests(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(
            f"/person/{str(self.person.id)}/delete/")
        self.no_response = self.client.get("/person/20/delete/")

    def test_person_delete_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_person_delete_status_code_404(self):
        self.assertEqual(self.no_response.status_code, 404)

    def test_person_delete_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "persons/person_delete.html")

    def test_person_delete_contains(self):
        self.assertContains(self.response, "Ylmaz Zett")

    def test_person_delete_contains_not(self):
        self.assertNotContains(self.response, "Bye")

    def test_person_delete_resolves_personupdateview(self):
        view = resolve(f'/person/{str(self.person.id)}/delete/')
        self.assertEqual(view.func.__name__,
                         PersonDeleteView.as_view().__name__)
