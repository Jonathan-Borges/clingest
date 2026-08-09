from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import MovimentacaoFinanceiraForm
from .models import MovimentacaoFinanceira
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce


@login_required
def lista_financeiro(request):

    movimentacoes = (
        MovimentacaoFinanceira.objects
        .select_related(
            "paciente",
            "profissional",
            "servico",
        )
        .order_by(
            "-data",
            "-id",
        )
    )

    receitas = (
        movimentacoes.filter(
            tipo="RECEITA",
            status="PAGO",
        )
        .aggregate(
    total=Coalesce(
        Sum("valor"),
        0,
        output_field=DecimalField(),
    )
)["total"]
    )

    despesas = (
        movimentacoes.filter(
            tipo="DESPESA",
            status="PAGO",
        )
        .aggregate(
    total=Coalesce(
        Sum("valor"),
        0,
        output_field=DecimalField(),
    )
)["total"]
    )

    pendentes = (
        movimentacoes.filter(
            status="PENDENTE",
        )
        .aggregate(
    total=Coalesce(
        Sum("valor"),
        0,
        output_field=DecimalField(),
    )
)["total"]
    )

    saldo = receitas - despesas

    return render(

        request,

        "financeiro/lista.html",

        {

            "movimentacoes": movimentacoes,

            "receitas": receitas,

            "despesas": despesas,

            "pendentes": pendentes,

            "saldo": saldo,

        },

    )


@login_required
def criar_movimentacao(request):

    if request.method == "POST":

        form = MovimentacaoFinanceiraForm(

            request.POST,

        )

        if form.is_valid():

            form.save()

            return redirect(

                "financeiro:lista",

            )

    else:

        form = MovimentacaoFinanceiraForm()

    return render(

        request,

        "financeiro/formulario.html",

        {

            "form": form,

        },

    )