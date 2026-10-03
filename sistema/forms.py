from django import forms
from .models import Cliente, Servico, Agendamento


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'cpf', 'ativo']

        widgets = {
            'telefone': forms.TextInput(attrs={
                'placeholder': '(47) 99999-9999'
            }),
            'cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00'
            }),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        numeros = ''.join(filter(str.isdigit, cpf))

        if len(numeros) != 11:
            raise forms.ValidationError('Digite um CPF válido.')

        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        numeros = ''.join(filter(str.isdigit, telefone))

        if len(numeros) not in [10, 11]:
            raise forms.ValidationError('Digite um telefone válido.')

        return telefone


class ServicoForm(forms.ModelForm):
    valor = forms.CharField(
        label='Preço',
        widget=forms.TextInput(attrs={
            'placeholder': 'R$ 600,00',
            'inputmode': 'decimal'
        })
    )

    duracao = forms.IntegerField(
        label='Duração em minutos',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ex: 120',
            'min': '1'
        })
    )

    class Meta:
        model = Servico
        fields = ['descricao', 'valor', 'duracao', 'ativo']

    def clean_valor(self):
        valor = self.cleaned_data['valor'].replace('R$', '').strip()
        valor = valor.replace('.', '').replace(',', '.')

        try:
            valor = float(valor)
        except ValueError:
            raise forms.ValidationError('Digite um preço válido.')

        if valor <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero.')

        return valor

    def clean_duracao(self):
        duracao = self.cleaned_data['duracao']

        if duracao <= 0:
            raise forms.ValidationError('A duração deve ser maior que zero.')

        return duracao


class AgendamentoForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    horario = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Agendamento
        fields = [
            'cliente',
            'servico',
            'data',
            'horario',
            'observacao',
            'status'
        ]

    def clean(self):
        dados = super().clean()

        cliente = dados.get('cliente')
        servico = dados.get('servico')
        data = dados.get('data')
        horario = dados.get('horario')

        if cliente and not cliente.ativo:
            raise forms.ValidationError(
                'Não é possível agendar para um cliente inativo.'
            )

        if servico and not servico.ativo:
            raise forms.ValidationError(
                'Não é possível agendar um serviço inativo.'
            )

        if data:
            from django.utils import timezone

            if data < timezone.localdate():
                raise forms.ValidationError(
                    'Não é possível fazer um agendamento para uma data passada.'
                )

        if data and horario and servico:
            from datetime import datetime, timedelta

            inicio_novo = datetime.combine(data, horario)
            fim_novo = inicio_novo + timedelta(minutes=servico.duracao)

            agendamentos = Agendamento.objects.filter(
                data=data,
                servico=servico
            )

            if self.instance.pk:
                agendamentos = agendamentos.exclude(
                    pk=self.instance.pk
                )

            for agendamento in agendamentos:
                inicio_existente = datetime.combine(
                    agendamento.data,
                    agendamento.horario
                )

                fim_existente = inicio_existente + timedelta(
                    minutes=agendamento.servico.duracao
                )

                if inicio_novo < fim_existente and fim_novo > inicio_existente:
                    raise forms.ValidationError(
                        'Este serviço já possui um agendamento neste período.'
                    )

        return dados