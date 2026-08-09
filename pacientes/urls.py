from django.urls import path

from . import views


app_name = "pacientes"


urlpatterns = [
    path(
        "",
        views.lista_pacientes,
        name="lista",
    ),

    path(
        "novo/",
        views.criar_paciente,
        name="criar",
    ),

    path(
        "<int:pk>/",
        views.detalhe_paciente,
        name="detalhe",
    ),

    path(
        "<int:pk>/editar/",
        views.editar_paciente,
        name="editar",
    ),

    path(
        "<int:pk>/excluir/",
        views.excluir_paciente,
        name="excluir",
    ),
]