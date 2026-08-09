from django.contrib import admin

from .models import Profissional
from .models import ProfissionalServico


@admin.register(Profissional)
class ProfissionalAdmin(admin.ModelAdmin):

    list_display = [
        "nome_completo",
        "cpf",
        "especialidade",
        "ativo",
        "data_cadastro",
    ]

    list_filter = [
        "ativo",
        "especialidade",
    ]

    search_fields = [
        "nome_completo",
        "cpf",
        "email",
    ]


@admin.register(ProfissionalServico)
class ProfissionalServicoAdmin(admin.ModelAdmin):

    list_display = [
        "profissional",
        "servico",
        "valor",
        "duracao_minutos",
        "ativo",
    ]

    list_filter = [
        "ativo",
        "servico",
    ]

    search_fields = [
        "profissional__nome_completo",
        "servico__nome",
    ]