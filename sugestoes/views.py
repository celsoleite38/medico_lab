import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Sintoma, AnaliseClinica, AnaliseSintoma
from .services import sugerir_causas, registrar_feedback
from evolucoes.models import Evolucao

logger = logging.getLogger(__name__)


@login_required
def analise_clinica(request, evolucao_id):
    """Fluxo principal: médico seleciona sintomas, vê sugestões e finaliza."""
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)

    if request.method == 'POST':
        acao = request.POST.get('acao')
        sintoma_ids = [int(i) for i in request.POST.getlist('sintomas') if i.isdigit()]

        if acao == 'analisar' and sintoma_ids:
            # Criar ou reutilizar análise
            analise = AnaliseClinica.objects.create(
                paciente=evolucao.paciente,
                medico=request.user,
            )
            for sid in sintoma_ids:
                AnaliseSintoma.objects.create(analise=analise, sintoma_id=sid)

            # Gerar sugestões
            resultados = sugerir_causas(sintoma_ids)

            return render(request, 'sugestoes/resultado_analise.html', {
                'evolucao': evolucao,
                'paciente': evolucao.paciente,
                'analise': analise,
                'sintomas_selecionados': Sintoma.objects.filter(id__in=sintoma_ids),
                'resultados': resultados,
            })

        elif acao == 'finalizar':
            analise_id = request.POST.get('analise_id')
            condicao_id = request.POST.get('condicao_escolhida')
            aceitou = request.POST.get('aceitou_sugestao') == 'on'
            analise = get_object_or_404(AnaliseClinica, id=analise_id, medico=request.user)
            registrar_feedback(analise, int(condicao_id) if condicao_id else None, aceitou)
            messages.success(request, 'Análise clinica registrada e aprendizado atualizado.')
            return redirect('prontuario:plano_evolucao', id=evolucao.paciente.id)

    # GET: listar sintomas para seleção
    sintomas = Sintoma.objects.all()
    return render(request, 'sugestoes/analise_clinica.html', {
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
        'sintomas': sintomas,
    })


@login_required
def buscar_sintomas(request):
    """Busca AJAX de sintomas."""
    q = request.GET.get('q', '').strip()
    qs = Sintoma.objects.all()
    if q:
        qs = qs.filter(nome__icontains=q)
    data = [{'id': s.id, 'nome': s.nome} for s in qs[:30]]
    return JsonResponse(data, safe=False)
