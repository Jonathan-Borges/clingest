from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import models

from .forms import ServicoForm
from .models import Servico
@login_required
def lista_servicos(request):


    busca = request.GET.get(
        "busca",
        "",
    ).strip()

    servicos = (
        Servico.objects
        .filter(
            ativo=True,
        )
        .prefetch_related(
            "profissionais_configurados",
        )
        .order_by(
            "nome",
        )
    )

    if busca:

        servicos = servicos.filter(

            models.Q(
                nome__icontains=busca,
            )
            |
            models.Q(
                descricao__icontains=busca,
            )

        )

    contexto = {

        "servicos": servicos,

        "busca": busca,

    }

    return render(
        request,
        "servicos/lista.html",
        contexto,
    )


@login_required
def criar_servico(request):

    if request.method == "POST":

        form = ServicoForm(
            request.POST
        )

        if form.is_valid():

            servico = form.save()

            return redirect(
                "servicos:detalhe",
                pk=servico.pk,
            )

    else:

        form = ServicoForm()

    contexto = {
        "form": form,
    }

    return render(
        request,
        "servicos/formulario.html",
        contexto,
    )


@login_required
def detalhe_servico(request, pk):

    servico = get_object_or_404(
        Servico,
        pk=pk,
    )

    profissionais = (
        servico.profissionais_configurados
        .select_related(
            "profissional",
        )
        .filter(
            profissional__ativo=True,
        )
        .order_by(
            "profissional__nome_completo",
        )
    )

    contexto = {

        "servico": servico,

        "profissionais": profissionais,

    }

    return render(
        request,
        "servicos/detalhe.html",
        contexto,
    )




@login_required
def editar_servico(request, pk):

    servico = get_object_or_404(
        Servico,
        pk=pk,
    )

    if request.method == "POST":

        form = ServicoForm(
            request.POST,
            instance=servico,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "servicos:detalhe",
                pk=servico.pk,
            )

    else:

        form = ServicoForm(
            instance=servico,
        )

    contexto = {
        "form": form,
        "servico": servico,
    }

    return render(
        request,
        "servicos/formulario.html",
        contexto,
    )


@login_required
def excluir_servico(request, pk):

    servico = get_object_or_404(
        Servico,
        pk=pk,
    )

    if request.method == "POST":

        servico.ativo = False

        servico.save()

        return redirect(
            "servicos:lista"
        )

    return render(
        request,
        "servicos/detalhe.html",
        {
            "servico": servico,
        },
    )