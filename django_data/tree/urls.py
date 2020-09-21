from django.urls import path
from .views import TreeView, ChooseAncestorView, download_png, download_pdf

urlpatterns = [
    path('', TreeView.as_view(), name='tree'),
    path('choose_ancestor', ChooseAncestorView.as_view(), name='choose_ancestor'),
    path('download_tree_png/<int:pk>/', download_png, name='download_tree_png'),
    path('download_tree_pdf/<int:pk>/', download_pdf, name='download_tree_pdf'),
]
