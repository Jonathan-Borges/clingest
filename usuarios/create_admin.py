import os

from django.core.management.base import BaseCommand
from usuarios.models import Usuario


class Command(BaseCommand):
    help = "Cria o usuário administrador usando variáveis de ambiente"

    def handle(self, *args, **options):
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_EMAIL ou DJANGO_SUPERUSER_PASSWORD não configurados."
                )
            )
            return

        usuario, criado = Usuario.objects.get_or_create(
            email=email,
            defaults={
                "nome": "Administrador",
                "tipo_usuario": Usuario.TipoUsuario.ADMINISTRADOR,
                "ativo": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if criado:
            usuario.set_password(password)
            usuario.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Administrador {email} criado com sucesso."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"O usuário {email} já existe."
                )
            )