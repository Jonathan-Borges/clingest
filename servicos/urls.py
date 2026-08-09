from django.urls import path

from . import views


app_name = "servicos"


urlpatterns = [

    path(
        "",
        views.lista_servicos,
        name="lista",
    ),

    path(
        "novo/",
        views.criar_servico,
        name="criar",
    ),

    path(
        "<int:pk>/",
        views.detalhe_servico,
        name="detalhe",
    ),

    path(
        "<int:pk>/editar/",
        views.editar_servico,
        name="editar",
    ),

    path(
        "<int:pk>/excluir/",
        views.excluir_servico,
        name="excluir",
    ),

]