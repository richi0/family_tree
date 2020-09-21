from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Person


class PersonListView(ListView):
    model = Person
    template_name = "persons/person_list.html"
    ordering = ['first_name']


class PersonDetailView(DetailView):
    model = Person
    template_name = "persons/person_detail.html"


class PersonCreateView(CreateView):
    model = Person
    template_name = "persons/person_create.html"
    fields = "__all__"


class PersonUpdateView(UpdateView):
    model = Person
    template_name = "persons/person_update.html"
    fields = "__all__"


class PersonDeleteView(DeleteView):
    model = Person
    template_name = "persons/person_delete.html"
    success_url = reverse_lazy('person_list')
