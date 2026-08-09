from django import forms
from datetime import date
from .models import MovimentacaoFinanceira


class MovimentacaoFinanceiraForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["data"].initial = date.today()


    class Meta:

            model = MovimentacaoFinanceira

            fields = [

                "tipo",

                "categoria",

                "paciente",

                "profissional",

                "servico",

                "valor",

                "forma_pagamento",

                "status",

                "data",

                "observacao",

            ]

            widgets = {

                "tipo": forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),

                "categoria": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "placeholder": "Ex.: Consulta Nutricional",
                    }
                ),

                "paciente": forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),

                "profissional": forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),

                "servico": forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),

                "valor": forms.NumberInput(
                    attrs={
                        "class": "form-control",
                        "step": "0.01",
                    }
                ),

                "forma_pagamento": forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),

                "status": forms.Select(
                    attrs={
                        "class": "form-select",
                    }
                ),

                "data": forms.DateInput(
                    attrs={
                        "class": "form-control",
                        "type": "date",
                    }
                ),

                "observacao": forms.Textarea(
                    attrs={
                        "class": "form-control",
                        "rows": 4,
                    }
                ),

            }