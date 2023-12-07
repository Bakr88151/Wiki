from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("results/", views.results, name="results"),
    path("new", views.new, name="new"),
    path("add", views.add, name="add"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("change", views.change, name="change"),
    path("random", views.random, name="random"),
]
