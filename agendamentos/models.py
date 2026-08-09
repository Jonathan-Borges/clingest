from django.db import models

from pacientes.models import Paciente
from profissionais.models import Profissional
from servicos.models import Servico


class Agendamento(models.Model):

    STATUS_AGENDADO = "AGENDADO"
    STATUS_CONFIRMADO = "CONFIRMADO"
    STATUS_REALIZADO = "REALIZADO"
    STATUS_CANCELADO = "CANCELADO"
    STATUS_FALTOU = "FALTOU"

    STATUS_CHOICES = [
        (
            STATUS_AGENDADO,
            "Agendado",
        ),
        (
            STATUS_CONFIRMADO,
            "Confirmado",
        ),
        (
            STATUS_REALIZADO,
            "Realizado",
        ),
        (
            STATUS_CANCELADO,
            "Cancelado",
        ),
        (
            STATUS_FALTOU,
            "Paciente faltou",
        ),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.PROTECT,
        related_name="agendamentos",
    )

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name="agendamentos",
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="agendamentos",
    )

    data = models.DateField()

    horario = models.TimeField()

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    duracao_minutos = models.PositiveIntegerField(
        default=60,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AGENDADO,
    )

    observacoes = models.TextField(
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
            "data",
            "horario",
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "profissional",
                    "data",
                    "horario",
                ],
                name="unique_profissional_horario",
            ),

        ]

    def __str__(self):

        return (
            f"{self.paciente} - "
            f"{self.profissional} - "
            f"{self.data} "
            f"{self.horario}"
        )