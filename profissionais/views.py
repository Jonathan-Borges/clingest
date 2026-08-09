from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Q
from django.db.models import Avg
from django.db.models import Count
from .forms import ProfissionalForm
from .forms import ProfissionalServicoForm
from .models import Profissional
from .models import ProfissionalServico
from django.db import models
@login_required
def lista_profissionais(request):

    busca = request.GET.get(
        "busca",
        "",
    ).strip()


    profissionais = (
Profissional.objects
.all()
.order_by(
"nome_completo",
)
)


    if busca:

        profissionais = profissionais.filter(

            Q(
                nome_completo__icontains=busca
            )
            |
            Q(
                cpf__icontains=busca
            )
            |
            Q(
                especialidade__icontains=busca
            )
            |
            Q(
                registro_profissional__icontains=busca
            )
            |
            Q(
                telefone__icontains=busca
            )
            |
            Q(
                email__icontains=busca
            )

        )


    contexto = {

        "profissionais": profissionais,

        "busca": busca,

    }


    return render(

        request,

        "profissionais/lista.html",

        contexto,

    )


@login_required
def criar_profissional(request):

    if request.method == "POST":

        form = ProfissionalForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "profissionais:lista"
            )

    else:

        form = ProfissionalForm()

        contexto = {

        "form": form,

    }

    return render(
        request,
        "profissionais/formulario.html",
        contexto,
    )


@login_required
def detalhe_profissional(request, pk):

    profissional = get_object_or_404(
        Profissional,
        pk=pk,
    )

    servicos = (
        ProfissionalServico.objects
        .filter(
            profissional=profissional,
        )
        .select_related(
            "servico",
        )
        .order_by(
            "servico__nome",
        )
    )

    estatisticas = servicos.aggregate(

        total=Count("id"),

        ativos=Count(
            "id",
            filter=models.Q(
                ativo=True,
            ),
        ),

        ticket=Avg("valor"),

        tempo=Avg("duracao_minutos"),

    )

    contexto = {

        "profissional": profissional,

        "servicos": servicos,

        "estatisticas": estatisticas,

    }

    return render(

        request,

        "profissionais/detalhe.html",

        contexto,

    )

@login_required
def editar_profissional(request, pk):

    profissional = get_object_or_404(
        Profissional,
        pk=pk,
    )

    if request.method == "POST":

        form = ProfissionalForm(
            request.POST,
            instance=profissional,
        )

        if form.is_valid():

            form.save()

            return redirect(
                "profissionais:detalhe",
                pk=profissional.pk,
            )

    else:

        form = ProfissionalForm(
            instance=profissional,
        )

    contexto = {

        "form": form,

        "profissional": profissional,

    }

    return render(
        request,
        "profissionais/formulario.html",
        contexto,
    )


@login_required
def excluir_profissional(request, pk):

    profissional = get_object_or_404(
        Profissional,
        pk=pk,
    )

    if request.method == "POST":

        profissional.ativo = False

        profissional.save(
            update_fields=[
                "ativo",
            ]
        )

    return redirect(
        "profissionais:lista"
    )


@login_required
def adicionar_servico(request, pk):

    profissional = get_object_or_404(

        Profissional,

        pk=pk,

    )


    if request.method == "POST":

        form = ProfissionalServicoForm(

            request.POST,

        )


        if form.is_valid():

            servico = form.cleaned_data[

                "servico"

            ]


            existe = ProfissionalServico.objects.filter(

                profissional=profissional,

                servico=servico,

            ).exists()


            if existe:

                form.add_error(

                    "servico",

                    "Este serviço já está cadastrado para este profissional.",

                )

            else:

                profissional_servico = form.save(

                    commit=False,

                )


                profissional_servico.profissional = (

                    profissional

                )


                profissional_servico.save()


                return redirect(

                    "profissionais:detalhe",

                    pk=profissional.pk,

                )

    else:

        form = ProfissionalServicoForm()


    contexto = {

        "form": form,

        "profissional": profissional,

    }


    return render(

        request,

        "profissionais/adicionar_servico.html",

        contexto,

    )
    
@login_required
def editar_servico(request, pk):

    profissional_servico = get_object_or_404(

        ProfissionalServico,

        pk=pk,

    )

    if request.method == "POST":

        form = ProfissionalServicoForm(

            request.POST,

            instance=profissional_servico,

        )

        if form.is_valid():

            form.save()

            return redirect(

                "profissionais:detalhe",

                pk=profissional_servico.profissional.pk,

            )

    else:

        form = ProfissionalServicoForm(

            instance=profissional_servico,

        )

    contexto = {

        "form": form,

        "profissional": profissional_servico.profissional,

        "edicao": True,

    }

    return render(

        request,

        "profissionais/adicionar_servico.html",

        contexto,

    )
    
@login_required
def desativar_servico(request, pk):

    profissional_servico = get_object_or_404(

        ProfissionalServico,

        pk=pk,

    )

    profissional_servico.ativo = False

    profissional_servico.save(

        update_fields=[
            "ativo",
        ]

    )

    return redirect(

        "profissionais:detalhe",

        pk=profissional_servico.profissional.pk,

    )
    
@login_required
def reativar_servico(request, pk):

    profissional_servico = get_object_or_404(

        ProfissionalServico,

        pk=pk,

    )

    profissional_servico.ativo = True

    profissional_servico.save(

        update_fields=[
            "ativo",
        ]

    )

    return redirect(

        "profissionais:detalhe",

        pk=profissional_servico.profissional.pk,

    )