from django.db import models

from pacientes.models import Paciente
from profissionais.models import Profissional
from servicos.models import Servico


class MovimentacaoFinanceira(models.Model):

    TIPO_CHOICES = [

        ("RECEITA", "Receita"),

        ("DESPESA", "Despesa"),

    ]


    STATUS_CHOICES = [

        ("PENDENTE", "Pendente"),

        ("PAGO", "Pago"),

        ("CANCELADO", "Cancelado"),

    ]


    FORMA_PAGAMENTO = [

        ("PIX", "Pix"),

        ("DINHEIRO", "Dinheiro"),

        ("CARTAO_CREDITO", "Cartão de Crédito"),

        ("CARTAO_DEBITO", "Cartão de Débito"),

        ("TRANSFERENCIA", "Transferência"),

    ]


    tipo = models.CharField(

        max_length=15,

        choices=TIPO_CHOICES,

    )


    categoria = models.CharField(

        max_length=100,

    )


    paciente = models.ForeignKey(

        Paciente,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )


    profissional = models.ForeignKey(

        Profissional,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )


    servico = models.ForeignKey(

        Servico,

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

    )
    
    agendamento = models.OneToOneField(
    "agendamentos.Agendamento",
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="movimentacao_financeira",
)


    valor = models.DecimalField(

        max_digits=10,

        decimal_places=2,

    )


    forma_pagamento = models.CharField(

        max_length=30,

        choices=FORMA_PAGAMENTO,

        blank=True,

    )

    

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="PENDENTE",

    )


    observacao = models.TextField(

        blank=True,

    )


    data = models.DateField()


    data_cadastro = models.DateTimeField(

        auto_now_add=True,

    )


    def __str__(self):

        return f"{self.categoria} - R$ {self.valor}"