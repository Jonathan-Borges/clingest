from django.db import migrations


def criar_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    grupos = [
        "Administrador",
        "Recepção",
        "Profissional",
        "Financeiro",
    ]

    for nome in grupos:
        Group.objects.get_or_create(name=nome)


def remover_grupos(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    grupos = [
        "Administrador",
        "Recepção",
        "Profissional",
        "Financeiro",
    ]

    Group.objects.filter(name__in=grupos).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            criar_grupos,
            remover_grupos,
        ),
    ]