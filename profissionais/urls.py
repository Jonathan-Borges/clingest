from django.urls import path

from . import views

app_name = "profissionais"

urlpatterns = [


path(
    "",
    views.lista_profissionais,
    name="lista",
),

path(
    "novo/",
    views.criar_profissional,
    name="criar",
),

path(
    "<int:pk>/",
    views.detalhe_profissional,
    name="detalhe",
),

path(
    "<int:pk>/editar/",
    views.editar_profissional,
    name="editar",
),

path(
    "<int:pk>/excluir/",
    views.excluir_profissional,
    name="excluir",
),

path(
    "<int:pk>/adicionar-servico/",
    views.adicionar_servico,
    name="adicionar_servico",
),

path(
    "servico/<int:pk>/editar/",
    views.editar_servico,
    name="editar_servico",
),

path(
    "servico/<int:pk>/desativar/",
    views.desativar_servico,
    name="desativar_servico",
),

path(
    "servico/<int:pk>/reativar/",
    views.reativar_servico,
    name="reativar_servico",
),

]
