from django.db import models

from agendamentos.models import Agendamento
from pacientes.models import Paciente
from profissionais.models import Profissional

class Atendimento(models.Model):


    STATUS_CHOICES = [
        ("EM_ANDAMENTO", "Em andamento"),
        ("FINALIZADO", "Finalizado"),
        ("CANCELADO", "Cancelado"),
    ]

    agendamento = models.OneToOneField(
        Agendamento,
        on_delete=models.PROTECT,
        related_name="atendimento",
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name="atendimentos",
    )

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name="atendimentos",
    )

    data_inicio = models.DateTimeField(
        auto_now_add=True,
    )

    data_fim = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="EM_ANDAMENTO",
    )

    queixa_principal = models.TextField(
        blank=True,
    )

    observacoes = models.TextField(
        blank=True,
    )

    conduta = models.TextField(
        blank=True,
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True,
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = [
            "-data_inicio",
        ]

    def __str__(self):

        return (
            f"{self.paciente} - "
            f"{self.profissional} - "
            f"{self.data_inicio:%d/%m/%Y %H:%M}"
        )
