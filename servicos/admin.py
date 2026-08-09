from django.contrib import admin

from .models import Servico


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):

    list_display = [
        "nome",
        "duracao_minutos",
        "valor",
        "ativo",
        "data_cadastro",
    ]

    list_filter = [
        "ativo",
    ]

    search_fields = [
        "nome",
        "descricao",
    ]