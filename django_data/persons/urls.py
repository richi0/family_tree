from django.urls import path
from .views import (PersonListView, PersonDetailView,
                    PersonCreateView, PersonUpdateView, PersonDeleteView)

urlpatterns = [
    path('', PersonListView.as_view(), name='person_list'),
    path('person/<int:pk>/', PersonDetailView.as_view(), name='person_detail'),
    path('person/<int:pk>/edit/', PersonUpdateView.as_view(), name='person_update'),
    path('person/<int:pk>/delete/',
         PersonDeleteView.as_view(), name='person_delete'),
    path('person/new/', PersonCreateView.as_view(), name='person_create'),
]
