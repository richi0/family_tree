from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

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

class SearchResultsListView(ListView):
    model = Person
    template_name = 'persons/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Person.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) |
                Q(date_of_birth__icontains=query) | Q(date_of_death__icontains=query) |
                Q(hometown__icontains=query)
                ).order_by("first_name")
