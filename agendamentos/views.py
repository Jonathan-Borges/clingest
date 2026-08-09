from datetime import date
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


from profissionais.models import Profissional
from profissionais.models import ProfissionalServico

from .forms import AgendamentoForm
from .models import Agendamento

import json

from django.views.decorators.http import require_POST



@login_required
@require_POST
def mover_agendamento(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    try:

        dados = json.loads(
            request.body
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Dados inválidos.",
            },
            status=400,
        )


    nova_data = dados.get(
        "data"
    )

    novo_horario = dados.get(
        "horario"
    )


    if not nova_data or not novo_horario:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Data ou horário não informado.",
            },
            status=400,
        )



    existe = (
        Agendamento.objects.filter(
            profissional=agendamento.profissional,
            data=nova_data,
            horario=novo_horario,
        )
        .exclude(
            pk=agendamento.pk
        )
        .exists()
    )


    if existe:

        return JsonResponse(
            {
                "sucesso": False,
                "erro": "Horário ocupado.",
            }
        )


    agendamento.data = nova_data

    agendamento.horario = novo_horario

    agendamento.save(
        update_fields=[
            "data",
            "horario",
            "data_atualizacao",
        ]
    )


    return JsonResponse(
        {
            "sucesso": True,
            "mensagem": (
                "Agendamento alterado com sucesso."
            ),
        }
    )


@login_required
def lista_agendamentos(request):

    agendamentos = (
        Agendamento.objects.select_related(
            "paciente",
            "profissional",
            "servico",
        )
        .all()
        .order_by(
            "-data",
            "-horario",
        )
    )


    busca = request.GET.get(
        "busca",
        "",
    ).strip()


    data_filtro = request.GET.get(
        "data",
        "",
    )


    profissional_filtro = request.GET.get(
        "profissional",
        "",
    )


    status_filtro = request.GET.get(
        "status",
        "",
    )


    if busca:

        agendamentos = agendamentos.filter(
            Q(
                paciente__nome_completo__icontains=busca
            )
            |
            Q(
                paciente__cpf__icontains=busca
            )
            |
            Q(
                paciente__telefone__icontains=busca
            )
        )


    if data_filtro:

        agendamentos = agendamentos.filter(
            data=data_filtro
        )


    if profissional_filtro:

        agendamentos = agendamentos.filter(
            profissional_id=profissional_filtro
        )


    if status_filtro:

        agendamentos = agendamentos.filter(
            status=status_filtro
        )


    profissionais = (
        Profissional.objects.filter(
            ativo=True
        )
        .order_by(
            "nome_completo"
        )
    )


    paginator = Paginator(
        agendamentos,
        15,
    )


    pagina = request.GET.get(
        "page"
    )


    agendamentos = paginator.get_page(
        pagina
    )


    contexto = {

        "agendamentos": agendamentos,

        "profissionais": profissionais,

        "data_filtro": data_filtro,

        "profissional_filtro": profissional_filtro,

        "status_filtro": status_filtro,

        "status_choices": Agendamento.STATUS_CHOICES,

        "busca": busca,

    }


    return render(
        request,
        "agendamentos/lista.html",
        contexto,
    )



@login_required
def criar_agendamento(request):


    if request.method == "POST":


        form = AgendamentoForm(
            request.POST
        )


        if form.is_valid():


            agendamento = form.save(
                commit=False
            )


            profissional_servico = (
                ProfissionalServico.objects.get(
                    profissional=agendamento.profissional,
                    servico=agendamento.servico,
                    ativo=True,
                )
            )


            agendamento.valor = (
                profissional_servico.valor
            )


            agendamento.duracao_minutos = (
                profissional_servico.duracao_minutos
            )


            agendamento.save()


            return redirect(
                f"/agendamentos/agenda/?data={agendamento.data}"
            )


    else:

     form = AgendamentoForm(
        initial={
            "data": request.GET.get("data"),
            "horario": request.GET.get("horario"),
        }
    )

            


    contexto = {

        "form": form,

    }


    return render(
        request,
        "agendamentos/form.html",
        contexto,
    )



@login_required
def servicos_profissional(
    request,
    profissional_id
):

    servicos = (
        ProfissionalServico.objects.filter(
            profissional_id=profissional_id,
            ativo=True,
        )
        .select_related(
            "servico"
        )
    )


    dados = []


    for item in servicos:

        dados.append({

            "id": item.servico.id,

            "nome": item.servico.nome,

            "valor": str(
                item.valor
            ),

            "duracao_minutos":
                item.duracao_minutos,

        })


    return JsonResponse({

        "servicos": dados

    })

@login_required
def detalhe_agendamento(
    request,
    pk,
):

    agendamento = get_object_or_404(

        Agendamento.objects.select_related(
            "paciente",
            "profissional",
            "servico",
        ),

        pk=pk,

    )


    return render(
        request,
        "agendamentos/detalhe.html",
        {
            "agendamento": agendamento
        },
    )



@login_required
def editar_agendamento(
    request,
    pk,
):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )


    if request.method == "POST":

        form = AgendamentoForm(
            request.POST,
            instance=agendamento,
        )


        if form.is_valid():

            agendamento = form.save(
                commit=False
            )


            profissional_servico = (
                ProfissionalServico.objects.filter(
                    profissional=agendamento.profissional,
                    servico=agendamento.servico,
                    ativo=True,
                )
                .first()
            )


            if profissional_servico:

                agendamento.valor = (
                    profissional_servico.valor
                )


                agendamento.duracao_minutos = (
                    profissional_servico.duracao_minutos
                )


            agendamento.save()


            return redirect(
                "agendamentos:detalhe",
                pk=agendamento.pk,
            )


    else:

        form = AgendamentoForm(
            instance=agendamento
        )


    return render(
        request,
        "agendamentos/form.html",
        {
            "form": form,
            "agendamento": agendamento,
            "editar": True,
        },
    )



@login_required
def cancelar_agendamento(
    request,
    pk,
):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )


    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_CANCELADO
        )


        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )


    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def confirmar_agendamento(
    request,
    pk,
):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )


    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_CONFIRMADO
        )


        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )


    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def realizar_agendamento(
    request,
    pk,
):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )


    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_REALIZADO
        )


        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )


    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def faltou_agendamento(
    request,
    pk,
):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )


    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_FALTOU
        )


        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )


    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



# ================================
# CALENDÁRIO
# ================================


@login_required
def agenda(request):

    data_selecionada = request.GET.get(
        "data"
    )


    if not data_selecionada:

        data_selecionada = date.today()


    agendamentos = (
        Agendamento.objects.select_related(
            "paciente",
            "profissional",
            "servico",
        )
        .filter(
            data=data_selecionada
        )
        .order_by(
            "horario"
        )
    )


    profissionais = (
        Profissional.objects.filter(
            ativo=True
        )
        .order_by(
            "nome_completo"
        )
    )


    return render(
        request,
        "agendamentos/agenda.html",
        {

            "agendamentos": agendamentos,

            "data_selecionada": data_selecionada,

            "profissionais": profissionais,

        },
    )

@login_required
def cancelar_agendamento(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_CANCELADO
        )

        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )

    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def confirmar_agendamento(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_CONFIRMADO
        )

        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )

    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def realizar_agendamento(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_REALIZADO
        )

        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )

    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def faltou_agendamento(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )

    if request.method == "POST":

        agendamento.status = (
            Agendamento.STATUS_FALTOU
        )

        agendamento.save(
            update_fields=[
                "status",
                "data_atualizacao",
            ]
        )

    return redirect(
        "agendamentos:detalhe",
        pk=agendamento.pk,
    )



@login_required
def agenda(request):

    data_selecionada = request.GET.get(
        "data"
    )


    if not data_selecionada:

        data_selecionada = date.today()



    agendamentos = (
        Agendamento.objects.select_related(
            "paciente",
            "profissional",
            "servico",
        )
        .filter(
            data=data_selecionada
        )
        .order_by(
            "horario"
        )
    )


    profissionais = (
        Profissional.objects.filter(
            ativo=True
        )
        .order_by(
            "nome_completo"
        )
    )


    contexto = {

        "agendamentos": agendamentos,

        "data_selecionada": data_selecionada,

        "profissionais": profissionais,

    }


    return render(
        request,
        "agendamentos/agenda.html",
        contexto,
    )



@login_required
def eventos(request):


    agendamentos = (
        Agendamento.objects.select_related(
            "paciente",
            "profissional",
            "servico",
        )
        .all()
    )


    eventos = []


    for agendamento in agendamentos:


        eventos.append({

            "id": agendamento.pk,


            "title":
                (
                    f"{agendamento.paciente.nome_completo} - "
                    f"{agendamento.servico.nome}"
                ),


            "start":
                (
                    f"{agendamento.data}T"
                    f"{agendamento.horario.strftime('%H:%M:%S')}"
                ),


            "color":
                escolher_cor_status(
                    agendamento.status
                ),


            "extendedProps": {

                "paciente":
                    agendamento.paciente.nome_completo,


                "profissional":
                    agendamento.profissional.nome_completo,


                "servico":
                    agendamento.servico.nome,


                "horario":
                    agendamento.horario.strftime(
                        "%H:%M"
                    ),


                "data":
                    agendamento.data.strftime(
                        "%d/%m/%Y"
                    ),


                "valor":
                    str(
                        agendamento.valor
                    ),


                "status":
                    agendamento.get_status_display(),


                "status_codigo":
                    agendamento.status,


            }

        })


    return JsonResponse(
        eventos,
        safe=False
    )

def escolher_cor_status(status):


    cores = {


        "AGENDADO":
            "#0d6efd",


        "CONFIRMADO":
            "#198754",


        "REALIZADO":
            "#20c997",


        "CANCELADO":
            "#dc3545",


        "FALTOU":
            "#ffc107",

    }


    return cores.get(
        status,
        "#6c757d",
    )
    
@login_required
def finalizar_agendamento(request, pk):

    agendamento = get_object_or_404(
        Agendamento,
        pk=pk,
    )


    if request.method == "POST":

        agendamento.status = "REALIZADO"

        agendamento.save()


    return redirect(
        "agendamentos:lista"
    )