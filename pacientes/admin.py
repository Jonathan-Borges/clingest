from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):

    list_display = (
        "nome_completo",
        "cpf",
        "telefone",
        "email",
        "ativo",
        "data_cadastro",
    )

    list_filter = (
        "ativo",
        "data_cadastro",
    )

    search_fields = (
        "nome_completo",
        "cpf",
        "telefone",
        "email",
    )

    ordering = (
        "nome_completo",
    )