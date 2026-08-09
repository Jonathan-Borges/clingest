from django import forms

from .models import Profissional
from .models import ProfissionalServico

class ProfissionalForm(forms.ModelForm):

    class Meta:

        model = Profissional

        fields = [
            "nome_completo",
            "cpf",
            "especialidade",
            "registro_profissional",
            "telefone",
            "email",
        ]

        widgets = {

            "nome_completo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nome completo",
                }
            ),

            "cpf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "000.000.000-00",
                }
            ),

            "especialidade": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "registro_profissional": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Registro profissional",
                }
            ),

            "telefone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "(27) 99999-9999",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "profissional@clinica.com",
                }
            ),

        }

class ProfissionalServicoForm(forms.ModelForm):

    class Meta:

        model = ProfissionalServico

        fields = [
            "servico",
            "valor",
            "duracao_minutos",
            "ativo",
        ]

        widgets = {

            "servico": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0,00",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "duracao_minutos": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: 60",
                    "min": "1",
                }
            ),

            "ativo": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),

        }

def clean(self):

    cleaned_data = super().clean()

    profissional = getattr(
        self.instance,
        "profissional",
        None,
    )

    servico = cleaned_data.get(
        "servico",
    )

    if profissional and servico:

        existe = ProfissionalServico.objects.filter(

            profissional=profissional,

            servico=servico,

        ).exclude(

            pk=self.instance.pk,

        ).exists()

        if existe:

            raise forms.ValidationError(

                "Este serviço já está cadastrado para este profissional."

            )

    return cleaned_data