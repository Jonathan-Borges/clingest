from django.urls import path

from . import views

app_name = "atendimentos"

urlpatterns = [


path(
    "",
    views.lista_atendimentos,
    name="lista",
),


]
