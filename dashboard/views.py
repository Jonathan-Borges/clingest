
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from agendamentos.models import Agendamento
from pacientes.models import Paciente
from profissionais.models import Profissional
from servicos.models import Servico


@login_required
def dashboard(request):

    hoje = date.today()


    # ==========================================
    # TOTAIS GERAIS
    # ==========================================

    total_pacientes = (
        Paciente.objects
        .filter(
            ativo=True,
        )
        .count()
    )


    total_profissionais = (
        Profissional.objects
        .filter(
            ativo=True,
        )
        .count()
    )


    total_servicos = (
        Servico.objects
        .filter(
            ativo=True,
        )
        .count()
    )


    # ==========================================
    # AGENDAMENTOS DE HOJE
    # ==========================================

    agendamentos_hoje = (
        Agendamento.objects
        .filter(
            data=hoje,
        )
        .select_related(
            "paciente",
            "profissional",
            "servico",
        )
        .order_by(
            "horario",
        )
    )


    total_agendamentos_hoje = (
        agendamentos_hoje.count()
    )


    # ==========================================
    # FATURAMENTO DE HOJE
    # ==========================================

    faturamento_hoje = sum(

        (
            agendamento.valor
            or 0
        )

        for agendamento
        in agendamentos_hoje

    )


    # ==========================================
    # ATENDIMENTOS REALIZADOS
    # ==========================================

    atendimentos_realizados_hoje = (

        agendamentos_hoje

        .filter(
            status=Agendamento.STATUS_REALIZADO,
        )

        .count()

    )


    # ==========================================
    # CANCELAMENTOS
    # ==========================================

    cancelamentos_hoje = (

        agendamentos_hoje

        .filter(
            status=Agendamento.STATUS_CANCELADO,
        )

        .count()

    )


    # ==========================================
    # PRÓXIMO ATENDIMENTO
    # ==========================================

    agora = None

    try:

        from datetime import datetime

        agora = datetime.now().time()

    except Exception:

        agora = None


    proximo_agendamento = None


    if agora:

        proximo_agendamento = (

            agendamentos_hoje

            .filter(
                horario__gte=agora,
            )

            .exclude(
                status__in=[
                    Agendamento.STATUS_CANCELADO,
                    Agendamento.STATUS_FALTOU,
                ]
            )

            .first()

        )


    # ==========================================
    # CONTEXTO
    # ==========================================

    contexto = {

        "total_pacientes":
            total_pacientes,

        "total_profissionais":
            total_profissionais,

        "total_servicos":
            total_servicos,

        "agendamentos_hoje":
            agendamentos_hoje,

        "total_agendamentos_hoje":
            total_agendamentos_hoje,

        "faturamento_hoje":
            faturamento_hoje,

        "atendimentos_realizados_hoje":
            atendimentos_realizados_hoje,

        "cancelamentos_hoje":
            cancelamentos_hoje,

        "proximo_agendamento":
            proximo_agendamento,

    }


    return render(

        request,

        "dashboard/index.html",

        contexto,

    )

