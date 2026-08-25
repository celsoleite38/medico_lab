import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date
from .models import ModeloAtestado, Atestado
from .forms import AtestadoForm
from evolucoes.models import Evolucao

logger = logging.getLogger(__name__)


@login_required
def lista_atestados(request):
    """Lista todos os atestados emitidos pelo médico logado."""
    atestados = Atestado.objects.filter(
        medico=request.user
    ).select_related('evolucao', 'evolucao__paciente', 'modelo')

    q = request.GET.get('q', '').strip()
    if q:
        atestados = atestados.filter(
            Q(evolucao__paciente__nome__icontains=q) |
            Q(modelo__nome__icontains=q)
        ).distinct()

    return render(request, 'atestados/lista_atestados.html', {'atestados': atestados, 'query': q})


@login_required
def modelos_atestado(request, paciente_id=None):
    """Lista modelos de atestado. Se paciente_id fornecido, linka direto ao paciente."""
    modelos = ModeloAtestado.objects.filter(ativo=True)
    return render(request, 'atestados/modelos_atestado.html', {
        'modelos': modelos,
        'paciente_id': paciente_id,
    })


@login_required
def novo_atestado(request, evolucao_id=None, modelo_id=None, paciente_id=None):
    """Cria novo atestado. Aceita evolucao_id ou paciente_id (usa evolução mais recente)."""
    if evolucao_id:
        evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    elif paciente_id:
        from prontuario.models import Pacientes
        paciente = get_object_or_404(Pacientes, id=paciente_id, medico=request.user)
        evolucao = Evolucao.objects.filter(paciente=paciente).order_by('-data_criacao').first()
        if not evolucao:
            messages.error(request, 'Crie pelo menos uma evolução antes de emitir atestados.')
            return redirect('prontuario:dados_paciente', id=paciente.id)
    else:
        return redirect('prontuario:pacientes')
    modelo = get_object_or_404(ModeloAtestado, id=modelo_id, ativo=True)

    if request.method == 'POST':
        form = AtestadoForm(request.POST, modelo=modelo)
        if form.is_valid():
            atestado = form.save(commit=False)
            atestado.evolucao = evolucao
            atestado.medico = request.user
            atestado.texto_final = atestado.renderizar()
            atestado.save()

            messages.success(request, 'Atestado emitido com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
    else:
        form = AtestadoForm(modelo=modelo)

    return render(request, 'atestados/novo_atestado.html', {
        'form': form,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
        'modelo': modelo,
    })


@login_required
def atestado_pdf(request, atestado_id):
    atestado = get_object_or_404(
        Atestado, id=atestado_id,
        evolucao__paciente__medico=request.user
    )

    if not atestado.texto_final:
        atestado.texto_final = atestado.renderizar()
        atestado.save()

    html_string = render_to_string('atestados/atestado_pdf.html', {
        'atestado': atestado,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="atestado_{atestado.id}.pdf"'
    response.write(HTML(string=html_string).write_pdf())
    return response
