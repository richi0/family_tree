from django.test import TestCase
from django.urls import reverse, resolve

from .views import (TreeView, ChooseAncestorView, download_pdf, download_png)
from persons.models import Person
from persons.tests import create_person


class ChooseAncestorTests(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(reverse("choose_ancestor"))

    def test_choose_ancestor_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_choose_ancestor_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "tree/choose_ancestor.html")

    def test_choose_ancestor_contains(self):
        self.assertContains(self.response, "Ylmaz")

    def test_choose_ancestor_contains_not(self):
        self.assertNotContains(self.response, "Hello")

    def test_choose_ancestor_resolves_chooseancesterview(self):
        view = resolve(reverse("choose_ancestor"))
        self.assertEqual(view.func.__name__,
                         ChooseAncestorView.as_view().__name__)


class TreeTests(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(reverse("tree") + "?pk=1")

    def test_tree_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tree_template(self):
        self.assertTemplateUsed(self.response, "persons/base.html")
        self.assertTemplateUsed(self.response, "tree/tree.html")

    def test_tree_contains(self):
        self.assertContains(self.response, "Download")

    def test_tree_contains_not(self):
        self.assertNotContains(self.response, "jpeg")

    def test_tree_resolves_treeview(self):
        view = resolve(reverse("tree"))
        self.assertEqual(view.func.__name__, TreeView.as_view().__name__)


class TreeDownloadPdf(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(
            reverse("download_tree_pdf", args=[1]))
        self.no_response = self.client.get(
            reverse("download_tree_pdf", args=[2]))

    def test_tree_download_pdf_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tree_download_pdf__bad_status_code(self):
        self.assertEqual(self.no_response.status_code, 404)


class TreeDownloadPng(TestCase):
    def setUp(self):
        self.person = create_person()
        self.response = self.client.get(
            reverse("download_tree_png", args=[1]))
        self.no_response = self.client.get(
            reverse("download_tree_png", args=[2]))

    def test_tree_download_png_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_tree_download_png__bad_status_code(self):
        self.assertEqual(self.no_response.status_code, 404)
