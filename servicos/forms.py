from django import forms

from .models import Servico


class ServicoForm(forms.ModelForm):

    class Meta:

        model = Servico

        fields = [
            "nome",
            "descricao",
            "duracao_minutos",
            "valor",
        ]

        widgets = {

            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex.: Consulta Nutricional",
                }
            ),

            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descrição do serviço",
                }
            ),

            "duracao_minutos": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "Ex.: 60",
                }
            ),

            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Ex.: 150.00",
                }
            ),
        }