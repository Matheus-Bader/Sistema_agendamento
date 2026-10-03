from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Cliente, Servico, Agendamento
from .forms import ClienteForm, ServicoForm, AgendamentoForm

@login_required
def inicio(request):
    hoje = timezone.localdate()

    clientes = Cliente.objects.count()
    servicos = Servico.objects.filter(ativo=True).count()
    agendamentos_hoje = Agendamento.objects.filter(data=hoje).count()
    agendamentos_realizados = Agendamento.objects.filter(status='REALIZADO').count()

    context = {
        'clientes': clientes,
        'servicos': servicos,
        'agendamentos_hoje': agendamentos_hoje,
        'agendamentos_realizados': agendamentos_realizados,
    }

    return render(request, 'inicio.html', context)


@login_required
def lista_clientes(request):
    busca = request.GET.get('busca', '')

    clientes = Cliente.objects.all()

    if busca:
        clientes = clientes.filter(nome__icontains=busca)

    return render(request, 'clientes/lista.html', {
        'clientes': clientes,
        'busca': busca
    })


@login_required
def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/formulario.html', {
        'form': form,
        'titulo': 'Novo Cliente'
    })


@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/formulario.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })


@login_required
def excluir_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('lista_clientes')

    return render(request, 'clientes/excluir.html', {
        'cliente': cliente
    })


@login_required
def alterar_status_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.ativo = not cliente.ativo
        cliente.save()

    return redirect('lista_clientes')


@login_required
def lista_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos/lista.html', {
        'servicos': servicos
    })


@login_required
def novo_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso!')
            return redirect('lista_servicos')
    else:
        form = ServicoForm()

    return render(request, 'servicos/formulario.html', {
        'form': form,
        'titulo': 'Novo Serviço'
    })


@login_required
def editar_servico(request, id):
    servico = get_object_or_404(Servico, id=id)

    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('lista_servicos')
    else:
        form = ServicoForm(instance=servico)

    return render(request, 'servicos/formulario.html', {
        'form': form,
        'titulo': 'Editar Serviço'
    })


@login_required
def excluir_servico(request, id):
    servico = get_object_or_404(Servico, id=id)

    if request.method == 'POST':
        servico.delete()
        messages.success(request, 'Serviço excluído com sucesso!')
        return redirect('lista_servicos')

    return render(request, 'servicos/excluir.html', {
        'servico': servico
    })


@login_required
def alterar_status_servico(request, id):
    servico = get_object_or_404(Servico, id=id)

    if request.method == 'POST':
        servico.ativo = not servico.ativo
        servico.save()

    return redirect('lista_servicos')


@login_required
def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all().order_by('data', 'horario')
    agora = timezone.localtime()

    for agendamento in agendamentos:
        agendamento.pode_registrar_chegada = (
            agendamento.data == agora.date()
            and agendamento.horario <= agora.time()
        )

    return render(request, 'agendamentos/lista.html', {
        'agendamentos': agendamentos
    })



@login_required
def novo_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento cadastrado com sucesso!')
            return redirect('lista_agendamentos')
    else:
        form = AgendamentoForm()

    return render(request, 'agendamentos/formulario.html', {
        'form': form,
        'titulo': 'Novo Agendamento'
    })


@login_required
def editar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)

    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)

        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('lista_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)

    return render(request, 'agendamentos/formulario.html', {
        'form': form,
        'titulo': 'Editar Agendamento'
    })


@login_required
def excluir_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)

    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso!')
        return redirect('lista_agendamentos')

    return render(request, 'agendamentos/excluir.html', {
        'agendamento': agendamento
    })


@login_required
def alterar_status_agendamento(request, id, status):
    agendamento = get_object_or_404(Agendamento, id=id)

    if request.method == 'POST':
        if status in ['AGENDADO', 'REALIZADO', 'CANCELADO']:
            agendamento.status = status
            agendamento.save()

    return redirect('lista_agendamentos')

@login_required
def registrar_chegada(request, id, chegou):
    agendamento = get_object_or_404(Agendamento, id=id)

    if request.method == 'POST':
        if chegou == 'sim':
            agendamento.chegou = True
            agendamento.status = 'REALIZADO'
        elif chegou == 'nao':
            agendamento.chegou = False
            agendamento.status = 'CANCELADO'

        agendamento.save()

    return redirect('lista_agendamentos')