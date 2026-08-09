from django import forms

from profissionais.models import ProfissionalServico

from .models import Agendamento


class AgendamentoForm(forms.ModelForm):

    class Meta:

        model = Agendamento

        fields = [
            "paciente",
            "profissional",
            "servico",
            "data",
            "horario",
            "valor",
            "status",
            "observacoes",
        ]
        localized_fields = []
        widgets = {

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

            "data": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "horario": forms.TimeInput(
    format="%H:%M",
    attrs={
        "class": "form-control",
        "type": "time",
    }
),

            "valor": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "readonly": True,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "observacoes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),

        }

    def clean(self):

        cleaned_data = super().clean()

        profissional = cleaned_data.get(
            "profissional"
        )

        servico = cleaned_data.get(
            "servico"
        )

        data = cleaned_data.get(
            "data"
        )

        horario = cleaned_data.get(
            "horario"
        )

        valor = cleaned_data.get(
            "valor"
        )


        # ==========================================
        # VALIDAR PROFISSIONAL + SERVIÇO
        # ==========================================

        profissional_servico = None

        if profissional and servico:

            profissional_servico = (
                ProfissionalServico.objects.filter(
                    profissional=profissional,
                    servico=servico,
                    ativo=True,
                )
                .first()
            )

            if not profissional_servico:

                raise forms.ValidationError(
                    "Este serviço não está "
                    "disponível para o profissional "
                    "selecionado."
                )


        # ==========================================
        # VALIDAR VALOR
        # ==========================================

        if profissional_servico and valor:

            if valor != profissional_servico.valor:

                raise forms.ValidationError(
                    "O valor informado não corresponde "
                    "ao valor configurado para este "
                    "serviço."
                )


        # ==========================================
        # VALIDAR HORÁRIO
        # ==========================================

        if (
            profissional
            and data
            and horario
        ):

            existe = (
                Agendamento.objects.filter(
                    profissional=profissional,
                    data=data,
                    horario=horario,
                )
                .exists()
            )

            if existe:

                raise forms.ValidationError(
                    "Este profissional já possui "
                    "um agendamento nesta data "
                    "e horário."
                )


        return cleaned_data