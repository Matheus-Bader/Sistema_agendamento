from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    cpf = models.CharField(max_length=14)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    duracao = models.IntegerField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao

    @property
    def duracao_formatada(self):
        horas = self.duracao // 60
        minutos = self.duracao % 60

        if horas > 0 and minutos > 0:
            return f'{horas}h {minutos}min'
        if horas > 0:
            return f'{horas}h'
        return f'{minutos}min'

    @property
    def valor_formatado(self):
        valor = f'{self.valor:,.2f}'
        valor = valor.replace(',', 'X').replace('.', ',').replace('X', '.')
        return f'R$ {valor}'


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data = models.DateField()
    horario = models.TimeField()
    observacao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AGENDADO'
    )
    chegou = models.BooleanField(null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.cliente} - {self.servico} - {self.data} {self.horario}'