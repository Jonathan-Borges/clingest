from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Agendamento

from financeiro.models import MovimentacaoFinanceira


@receiver(post_save, sender=Agendamento)
def criar_movimentacao_financeira(sender, instance, created, **kwargs):

    if instance.status == "REALIZADO":

        existe = MovimentacaoFinanceira.objects.filter(
    agendamento=instance,
).exists()


        if not existe:

            MovimentacaoFinanceira.objects.create(

    tipo="RECEITA",

    categoria=(
        f"{instance.servico.nome} - "
        f"{instance.paciente.nome_completo}"
    ),

    paciente=instance.paciente,

    profissional=instance.profissional,

    servico=instance.servico,

    agendamento=instance,

    valor=instance.valor,

    status="PAGO",

    data=instance.data,

    observacao=(
        "Receita gerada automaticamente "
        "pelo atendimento realizado."
    ),

)