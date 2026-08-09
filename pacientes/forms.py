from django import forms

from .models import Paciente

class PacienteForm(forms.ModelForm):

    class Meta:

        model = Paciente

        fields = [
            "nome_completo",
            "cpf",
            "data_nascimento",
            "telefone",
            "email",
            "endereco",
            "observacoes",
        ]

        widgets = {

            "nome_completo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o nome completo",
                }
            ),

            "cpf": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "000.000.000-00",
                }
            ),

            "data_nascimento": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "telefone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "(00) 00000-0000",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "paciente@email.com",
                }
            ),

            "endereco": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Rua, número, bairro, cidade...",
                }
            ),

            "observacoes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Informações adicionais sobre o paciente...",
                }
            ),

        }

        labels = {

            "nome_completo": "Nome completo",

            "cpf": "CPF",

            "data_nascimento": "Data de nascimento",

            "telefone": "Telefone",

            "email": "E-mail",

            "endereco": "Endereço",

            "observacoes": "Observações",

        }

        help_texts = {

            "cpf": "Informe o CPF do paciente.",

            "data_nascimento": "Selecione a data de nascimento.",

            "telefone": "Informe um telefone para contato.",

            "email": "Campo opcional.",

            "observacoes": "Adicione informações relevantes para o atendimento.",

        }