from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Atendimento

@login_required
def lista_atendimentos(request):


    atendimentos = (
        Atendimento.objects
        .select_related(
            "paciente",
            "profissional",
            "agendamento",
        )
        .order_by(
            "-data_inicio",
        )
    )

    contexto = {
        "atendimentos": atendimentos,
    }

    return render(
        request,
        "atendimentos/lista.html",
        contexto,
    )

