# evolucoes/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from prontuario.models import Pacientes
from .models import Evolucao


@login_required
def detalhe_evolucao(request, evolucao_id):
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    paciente = evolucao.paciente

    context = {
        'evolucao': evolucao,
        'paciente': paciente,
    }

    return render(request, 'evolucoes/detalhe_evolucao.html', context)
