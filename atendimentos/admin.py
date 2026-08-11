from django.contrib import admin

from .models import Atendimento

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):


    list_display = (
        "paciente",
        "profissional",
        "agendamento",
        "status",
        "data_inicio",
    )

    list_filter = (
        "status",
        "profissional",
        "data_inicio",
    )

    search_fields = (
        "paciente__nome_completo",
        "profissional__nome_completo",
    )
