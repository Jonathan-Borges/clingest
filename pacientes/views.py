from datetime import date

from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render

from agendamentos.models import Agendamento
from .forms import PacienteForm
from .models import Paciente


@login_required
def lista_pacientes(request):

    busca = request.GET.get(
        "busca",
        "",
    ).strip()

    pacientes = Paciente.objects.all()

    if busca:

        busca_normalizada = (
            busca.replace(".", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
            .lower()
        )

        pacientes_filtrados = []

        for paciente in pacientes:

            nome = (
                paciente.nome_completo or ""
            ).lower()

            cpf = (
                paciente.cpf or ""
            ).replace(
                ".",
                "",
            ).replace(
                "-",
                "",
            ).replace(
                "(",
                "",
            ).replace(
                ")",
                "",
            ).replace(
                " ",
                "",
            ).lower()

            telefone = (
                paciente.telefone or ""
            ).replace(
                ".",
                "",
            ).replace(
                "-",
                "",
            ).replace(
                "(",
                "",
            ).replace(
                ")",
                "",
            ).replace(
                " ",
                "",
            ).lower()

            email = (
                paciente.email or ""
            ).lower()

            if (
                busca_normalizada in nome
                or busca_normalizada in cpf
                or busca_normalizada in telefone
                or busca_normalizada in email
            ):
                pacientes_filtrados.append(
                    paciente.pk
                )

        pacientes = Paciente.objects.filter(
            pk__in=pacientes_filtrados
        )

    contexto = {
        "pacientes": pacientes,
        "busca": busca,
    }

    return render(
        request,
        "pacientes/lista.html",
        contexto,
    )


@login_required
def criar_paciente(request):

    if request.method == "POST":

        form = PacienteForm(
            request.POST,
        )

        if form.is_valid():

            paciente = form.save()

            return redirect(
                "pacientes:detalhe",
                pk=paciente.pk,
            )

    else:

        form = PacienteForm()

    contexto = {
        "form": form,
    }

    return render(
        request,
        "pacientes/formulario.html",
        contexto,
    )


@login_required
def detalhe_paciente(request, pk):

    paciente = get_object_or_404(
        Paciente,
        pk=pk,
    )

    agendamentos = (
        Agendamento.objects.filter(
            paciente=paciente,
        )
        .select_related(
            "profissional",
            "servico",
        )
        .order_by(
            "-data",
            "-horario",
        )
    )

    financeiro = (
        paciente.movimentacaofinanceira_set.all()
        .order_by("-data")
    )

    total_pago = financeiro.filter(
        status="PAGO",
        tipo="RECEITA",
    ).aggregate(
        total=models.Sum("valor")
    )["total"] or 0

    total_atendimentos = agendamentos.count()

    proximo_agendamento = (
        agendamentos.filter(
            data__gte=date.today(),
        )
        .order_by(
            "data",
            "horario",
        )
        .first()
    )

    ultimo_agendamento = (
        agendamentos.filter(
            data__lt=date.today(),
        )
        .first()
    )

    ultimo_pagamento = (
        financeiro.filter(
            status="PAGO",
        )
        .first()
    )

    faturamento_total = total_pago

    contexto = {
        "paciente": paciente,
        "agendamentos": agendamentos,
        "financeiro": financeiro,
        "total_pago": total_pago,
        "total_atendimentos": total_atendimentos,
        "proximo_agendamento": proximo_agendamento,
        "ultimo_agendamento": ultimo_agendamento,
        "ultimo_pagamento": ultimo_pagamento,
        "faturamento_total": faturamento_total,
    }

    return render(
        request,
        "pacientes/detalhe.html",
        contexto,
    )

@login_required
def editar_paciente(request, pk):

    paciente = get_object_or_404(
        Paciente,
        pk=pk,
    )

    if request.method == "POST":

        form = PacienteForm(
            request.POST,
            instance=paciente,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "pacientes:detalhe",
                pk=paciente.pk,
            )

    else:

        form = PacienteForm(
            instance=paciente,
        )

    contexto = {
        "form": form,
        "paciente": paciente,
    }

    return render(
        request,
        "pacientes/formulario.html",
        contexto,
    )


@login_required
def excluir_paciente(request, pk):

    paciente = get_object_or_404(
        Paciente,
        pk=pk,
    )

    if request.method == "POST":

        paciente.ativo = False
        paciente.save()

        return redirect(
            "pacientes:lista",
        )

    return render(
        request,
        "pacientes/detalhe.html",
        {
            "paciente": paciente,
        },
    )