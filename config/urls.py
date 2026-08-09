from django.contrib import admin
from django.urls import include
from django.urls import path


urlpatterns = [

    path(
        "admin/",
        admin.site.urls,
    ),


    path(
        "dashboard/",
        include("dashboard.urls"),
    ),


    path(
        "pacientes/",
        include("pacientes.urls"),
    ),


    path(
        "profissionais/",
        include("profissionais.urls"),
    ),


    path(
        "servicos/",
        include("servicos.urls"),
    ),


    path(
        "agendamentos/",
        include("agendamentos.urls"),
    ),


    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    
    path(
    "financeiro/",
    include("financeiro.urls"),
),

]