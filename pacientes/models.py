from django.db import models


class Paciente(models.Model):

    nome_completo = models.CharField(
        max_length=150
    )

    cpf = models.CharField(
        max_length=14,
        unique=True
    )

    data_nascimento = models.DateField()

    telefone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    endereco = models.CharField(
        max_length=255,
        blank=True
    )

    observacoes = models.TextField(
        blank=True
    )

    ativo = models.BooleanField(
        default=True
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.nome_completo