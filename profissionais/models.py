from django.db import models

from servicos.models import Servico


class Profissional(models.Model):

    ESPECIALIDADE_CHOICES = [
        ("FISIOTERAPIA", "Fisioterapia"),
        ("NUTRICAO", "Nutrição"),
        ("PSICOLOGIA", "Psicologia"),
        ("ODONTOLOGIA", "Odontologia"),
        ("MEDICINA", "Medicina"),
        ("DERMATOLOGIA", "Dermatologia"),
        ("ENFERMAGEM", "Enfermagem"),
        ("FONOAUDIOLOGIA", "Fonoaudiologia"),
        ("TERAPIA_OCUPACIONAL", "Terapia Ocupacional"),
        ("OUTRA", "Outra"),
    ]

    nome_completo = models.CharField(
        max_length=150,
    )

    cpf = models.CharField(
        max_length=14,
        unique=True,
    )

    especialidade = models.CharField(
        max_length=50,
        choices=ESPECIALIDADE_CHOICES,
    )

    registro_profissional = models.CharField(
        max_length=50,
        blank=True,
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    servicos = models.ManyToManyField(
        Servico,
        through="ProfissionalServico",
        related_name="profissionais",
        blank=True,
    )

    ativo = models.BooleanField(
        default=True,
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):

        return self.nome_completo


class ProfissionalServico(models.Model):

    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.CASCADE,
        related_name="servicos_configurados",
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.PROTECT,
        related_name="profissionais_configurados",
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    duracao_minutos = models.PositiveIntegerField(
        default=60,
    )

    ativo = models.BooleanField(
        default=True,
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "profissional",
                    "servico",
                ],
                name="profissional_servico_unico",
            ),

        ]

        ordering = [
            "profissional",
            "servico",
        ]

    def __str__(self):

        return (
            f"{self.profissional.nome_completo} - "
            f"{self.servico.nome}"
        )