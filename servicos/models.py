from django.db import models


class Servico(models.Model):

    nome = models.CharField(
        max_length=150,
        verbose_name="Nome do serviço",
    )

    descricao = models.TextField(
        blank=True,
        verbose_name="Descrição",
    )

    duracao_minutos = models.PositiveIntegerField(
        default=60,
        verbose_name="Duração em minutos",
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor",
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo",
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de cadastro",
    )

    def __str__(self):

        return self.nome

    class Meta:

        verbose_name = "Serviço"

        verbose_name_plural = "Serviços"

        ordering = [
            "nome",
        ]