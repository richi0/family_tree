import json

from django.views.generic import TemplateView, ListView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.http import HttpResponse, Http404

from persons.models import Person
from .createtree import Tree


class TreeView(TemplateView):
    template_name = "tree/tree.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        oldest = Person.objects.get(pk=int(self.request.GET["pk"]))
        tree = Tree()
        tree.build_tree(oldest)
        context['svg'] = tree.get_svg()
        context["pk"] = self.request.GET["pk"]
        return context


class ChooseAncestorView(ListView):
    model = Person
    template_name = "tree/choose_ancestor.html"
    ordering = ['first_name']


def get_file(request, pk, filetype, content_type):
    oldest = Person.objects.filter(pk=int(pk))
    if oldest.count():
        oldest = oldest[0]
        tree = Tree(filetype=filetype)
        tree.build_tree(oldest)
        response = HttpResponse(tree.get_file(), content_type=content_type)
        response['Content-Disposition'] = f"attachment; filename=family-tree.{filetype}"
        return response
    else:
        raise Http404


def download_png(request, pk):
    return get_file(request, pk, "png", content_type="image/png")


def download_pdf(request, pk):
    return get_file(request, pk, "pdf", content_type="application/pdf")
