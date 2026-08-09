from django.contrib.auth.models import BaseUserManager


class UsuarioManager(BaseUserManager):

    def create_user(self, email, nome, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa ter um e-mail.")

        email = self.normalize_email(email)

        usuario = self.model(
            email=email,
            nome=nome,
            **extra_fields
        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, nome, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault(
            "tipo_usuario",
            "ADMINISTRADOR"
        )

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superusuário precisa ter is_staff=True."
            )

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superusuário precisa ter is_superuser=True."
            )

        return self.create_user(
            email=email,
            nome=nome,
            password=password,
            **extra_fields
        )