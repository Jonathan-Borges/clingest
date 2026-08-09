from django.urls import path

from . import views

app_name = "financeiro"

urlpatterns = [

    path(

        "",

        views.lista_financeiro,

        name="lista",

    ),

    path(

        "novo/",

        views.criar_movimentacao,

        name="novo",

    ),

]