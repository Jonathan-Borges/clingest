from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UsuarioManager


class Usuario(AbstractUser):

    class TipoUsuario(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        RECEPCAO = "RECEPCAO", "Recepção"
        PROFISSIONAL = "PROFISSIONAL", "Profissional"
        FINANCEIRO = "FINANCEIRO", "Financeiro"

    username = None

    email = models.EmailField(
        unique=True
    )

    nome = models.CharField(
        max_length=150
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.RECEPCAO
    )

    ativo = models.BooleanField(
        default=True
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["nome"]

    objects = UsuarioManager()

    def __str__(self):
        return self.nome