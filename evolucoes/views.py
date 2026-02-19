# evolucoes/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from prontuario.models import Pacientes
from .models import Evolucao
from documentos.models import Receituario, PedidoExame, Atestado, ExameAnexado

@login_required
def detalhe_evolucao(request, evolucao_id):
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)  # segurança
    paciente = evolucao.paciente
    
    context = {
        'evolucao': evolucao,
        'paciente': paciente,
        'receituarios': evolucao.receituarios.all().order_by('-data_emissao'),
        'pedidos_exames': evolucao.pedidos_exames.all().order_by('-data_pedido'),
        'atestados': evolucao.atestados.all().order_by('-data_emissao'),
        'exames_anexados': evolucao.exames_anexados.all().order_by('-criado_em'),
    }
    
    print("Context enviado:", context)
    
    return render(request, 'evolucoes/detalhe_evolucao.html', context)