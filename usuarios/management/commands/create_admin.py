import os

from django.core.management.base import BaseCommand
from usuarios.models import Usuario


class Command(BaseCommand):
    help = "Cria o administrador inicial"

    def handle(self, *args, **options):
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(
                self.style.ERROR(
                    "As variáveis DJANGO_SUPERUSER_EMAIL e "
                    "DJANGO_SUPERUSER_PASSWORD precisam estar configuradas."
                )
            )
            return

        usuario = Usuario.objects.filter(email=email).first()

        if usuario:
            self.stdout.write(
                self.style.WARNING(
                    f"O usuário {email} já existe. Nenhum usuário foi criado."
                )
            )
            return

        usuario = Usuario(
            email=email,
            nome="Administrador",
            tipo_usuario="ADMINISTRADOR",
            ativo=True,
            is_staff=True,
            is_superuser=True,
        )

        usuario.set_password(password)
        usuario.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Administrador {email} criado com sucesso!"
            )
        )

