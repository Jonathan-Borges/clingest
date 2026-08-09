from django.urls import path

from . import views


app_name = "agendamentos"


urlpatterns = [

    path(
        "",
        views.lista_agendamentos,
        name="lista",
    ),


    path(
        "novo/",
        views.criar_agendamento,
        name="criar",
    ),


    path(
        "<int:pk>/",
        views.detalhe_agendamento,
        name="detalhe",
    ),


    path(
        "<int:pk>/editar/",
        views.editar_agendamento,
        name="editar",
    ),


    path(
        "<int:pk>/cancelar/",
        views.cancelar_agendamento,
        name="cancelar",
    ),


    # AJAX - carregar serviços do profissional

    path(
        "servicos-profissional/<int:profissional_id>/",
        views.servicos_profissional,
        name="servicos_profissional",
    ),

    path(
    "agenda/",
    views.agenda,
    name="agenda",
),


path(
    "eventos/",
    views.eventos,
    name="eventos",
),

path(
    "<int:pk>/confirmar/",
    views.confirmar_agendamento,
    name="confirmar",
),


path(
    "<int:pk>/realizar/",
    views.realizar_agendamento,
    name="realizar",
),


path(
    "<int:pk>/faltou/",
    views.faltou_agendamento,
    name="faltou",
),

path(
    "<int:pk>/mover/",
    views.mover_agendamento,
    name="mover",
),

path(
    "<int:pk>/finalizar/",
    views.finalizar_agendamento,
    name="finalizar",
),

]