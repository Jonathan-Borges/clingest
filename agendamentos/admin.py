from django.contrib import admin

from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):

    list_display = (
        "paciente",
        "profissional",
        "servico",
        "data",
        "horario",
        "valor",
        "status",
    )

    list_filter = (
        "status",
        "data",
        "profissional",
    )

    search_fields = (
        "paciente__nome_completo",
        "profissional__nome_completo",
        "servico__nome",
    )

    ordering = (
        "data",
        "horario",
    )