from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario

    list_display = (
        "email",
        "nome",
        "tipo_usuario",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "tipo_usuario",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "email",
        "nome",
        "telefone",
    )

    ordering = (
        "nome",
    )

    fieldsets = (
        (
            "Informações de acesso",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Informações pessoais",
            {
                "fields": (
                    "nome",
                    "telefone",
                    "tipo_usuario",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            "Criar usuário",
            {
                "classes": (
                    "wide",
                ),
                "fields": (
                    "email",
                    "nome",
                    "telefone",
                    "tipo_usuario",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )