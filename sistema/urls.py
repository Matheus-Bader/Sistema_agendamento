from django.urls import path
from . import views


urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/novo/', views.novo_cliente, name='novo_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:id>/', views.excluir_cliente, name='excluir_cliente'),
    path('clientes/status/<int:id>/', views.alterar_status_cliente, name='alterar_status_cliente'),
    path('servicos/', views.lista_servicos, name='lista_servicos'),
    path('servicos/novo/', views.novo_servico, name='novo_servico'),
    path('servicos/editar/<int:id>/', views.editar_servico, name='editar_servico'),
    path('servicos/excluir/<int:id>/', views.excluir_servico, name='excluir_servico'),
    path('servicos/status/<int:id>/', views.alterar_status_servico, name='alterar_status_servico'),
    path('agendamentos/', views.lista_agendamentos, name='lista_agendamentos'),
    path('agendamentos/novo/', views.novo_agendamento, name='novo_agendamento'),
    path('agendamentos/editar/<int:id>/', views.editar_agendamento, name='editar_agendamento'),
    path('agendamentos/excluir/<int:id>/', views.excluir_agendamento, name='excluir_agendamento'),
    path('agendamentos/status/<int:id>/<str:status>/', views.alterar_status_agendamento, name='alterar_status_agendamento'),
    path('agendamentos/chegada/<int:id>/<str:chegou>/', views.registrar_chegada, name='registrar_chegada'),
    
]