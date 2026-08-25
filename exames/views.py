import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date
from .models import Exame, PedidoExame, ItemPedidoExame, ResultadoExame, MedicaoResultado
from .forms import NovoPedidoExameForm, UploadResultadoForm
from .services import extrair_texto_pdf, interpretar_resultado
from evolucoes.models import Evolucao

logger = logging.getLogger(__name__)


@login_required
def lista_pedidos(request):
    """Lista todos os pedidos de exames do médico logado."""
    pedidos = PedidoExame.objects.filter(
        medico=request.user
    ).select_related('evolucao', 'evolucao__paciente').prefetch_related('itens', 'itens__exame')

    q = request.GET.get('q', '').strip()
    if q:
        pedidos = pedidos.filter(
            Q(evolucao__paciente__nome__icontains=q) |
            Q(itens__exame__nome__icontains=q)
        ).distinct()

    return render(request, 'exames/lista_pedidos.html', {'pedidos': pedidos, 'query': q})


@login_required
def lista_resultados(request):
    """Lista todos os resultados de exames do médico logado."""
    from prontuario.models import Pacientes
    pacientes = Pacientes.objects.filter(medico=request.user)
    resultados = ResultadoExame.objects.filter(paciente__in=pacientes).select_related('paciente')
    return render(request, 'exames/lista_resultados.html', {'resultados': resultados})


@login_required
def buscar_exames(request):
    """Busca AJAX de exames. Retorna JSON com exames ordenados por uso (favoritos primeiro)."""
    q = request.GET.get('q', '').strip()
    exclude_ids = request.GET.get('exclude', '')
    exclude = [int(i) for i in exclude_ids.split(',') if i.isdigit()]

    qs = Exame.objects.filter(ativo=True)
    if q:
        qs = qs.filter(nome__icontains=q)
    exames = qs.exclude(id__in=exclude)[:20]

    data = [{
        'id': e.id,
        'nome': e.nome,
        'categoria': e.get_categoria_display(),
        'uso_count': e.uso_count,
    } for e in exames]
    return JsonResponse(data, safe=False)


@login_required
def novo_pedido_exame(request, evolucao_id=None, paciente_id=None):
    """Cria novo pedido. Aceita evolucao_id ou paciente_id (usa evolução mais recente)."""
    if evolucao_id:
        evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    elif paciente_id:
        from prontuario.models import Pacientes
        paciente = get_object_or_404(Pacientes, id=paciente_id, medico=request.user)
        evolucao = Evolucao.objects.filter(paciente=paciente).order_by('-data_criacao').first()
        if not evolucao:
            messages.error(request, 'Crie pelo menos uma evolução antes de emitir pedidos.')
            return redirect('prontuario:dados_paciente', id=paciente.id)
    else:
        return redirect('prontuario:pacientes')

    if request.method == 'POST':
        form = NovoPedidoExameForm(request.POST)
        exame_ids = request.POST.getlist('exame_ids')
        instrucoes_map = {}
        for k, v in request.POST.items():
            if k.startswith('instrucoes_'):
                try:
                    eid = int(k.replace('instrucoes_', ''))
                    instrucoes_map[eid] = v
                except ValueError:
                    pass

        if form.is_valid() and exame_ids:
            pedido = form.save(commit=False)
            pedido.evolucao = evolucao
            pedido.medico = request.user
            pedido.save()

            for eid in exame_ids:
                try:
                    exame = Exame.objects.get(id=int(eid))
                    ItemPedidoExame.objects.create(
                        pedido=pedido,
                        exame=exame,
                        instrucoes=instrucoes_map.get(int(eid), ''),
                    )
                    # Incrementa uso
                    Exame.objects.filter(id=exame.id).update(uso_count=exame.uso_count + 1)
                except (Exame.DoesNotExist, ValueError):
                    pass

            messages.success(request, f'Pedido {pedido.id} criado com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
        else:
            if not exame_ids:
                messages.error(request, 'Selecione pelo menos um exame.')

    else:
        form = NovoPedidoExameForm()

    return render(request, 'exames/novo_pedido.html', {
        'form': form,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
    })


@login_required
def pedido_exame_pdf(request, pedido_id):
    pedido = get_object_or_404(
        PedidoExame, id=pedido_id,
        evolucao__paciente__medico=request.user
    )
    from autenticacao.models import PerfilProfissional
    perfil = PerfilProfissional.objects.filter(usuario=request.user).first()

    html_string = render_to_string('exames/pedido_exame_pdf.html', {
        'pedido': pedido,
        'perfil': perfil,
        'today': date.today(),
    })
    pdf = HTML(string=html_string).write_pdf()

    response = render(request, 'exames/pedido_exame_pdf.html', {
        'pedido': pedido,
        'perfil': perfil,
        'today': date.today(),
    })
    response = HTML(string=render_to_string('exames/pedido_exame_pdf.html', {
        'pedido': pedido, 'perfil': perfil, 'today': date.today(),
    })).write_pdf()

    from django.http import HttpResponse
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pedido_exame_{pedido.id}.pdf"'
    pdf_content = HTML(string=render_to_string('exames/pedido_exame_pdf.html', {
        'pedido': pedido, 'perfil': perfil, 'today': date.today(),
    })).write_pdf()
    response.write(pdf_content)
    return response


@login_required
def upload_resultado(request, paciente_id):
    from prontuario.models import Pacientes
    paciente = get_object_or_404(Pacientes, id=paciente_id, medico=request.user)

    if request.method == 'POST':
        form = UploadResultadoForm(request.POST, request.FILES)
        if form.is_valid():
            resultado = form.save(commit=False)
            resultado.paciente = paciente
            resultado.save()

            # Tenta extrair e interpretar se PDF
            if resultado.tipo == 'pdf':
                texto = extrair_texto_pdf(resultado.arquivo.path)
                resultado.texto_extraido = texto
                if texto:
                    interpretacao = interpretar_resultado(texto)
                    resultado.resumo_leitura = interpretacao['resumo']
                    resultado.leitura_ok = True
                    resultado.save()

                    # Salvar medições
                    for med in interpretacao['medicoes']:
                        MedicaoResultado.objects.create(
                            resultado=resultado,
                            analito=med['analito'],
                            valor=med['valor'],
                            unidade=med.get('unidade', ''),
                            referencia_min=med.get('min'),
                            referencia_max=med.get('max'),
                            status=med['status'],
                            orientacao=med.get('orientacao', ''),
                        )
                else:
                    resultado.resumo_leitura = "Não foi possível extrair texto deste PDF."
                    resultado.save()

            messages.success(request, 'Resultado anexado com sucesso.')
            return redirect('prontuario:dados_paciente', id=paciente.id)
    else:
        form = UploadResultadoForm()

    return render(request, 'exames/upload_resultado.html', {
        'form': form,
        'paciente': paciente,
    })


@login_required
def ver_resultado(request, resultado_id):
    resultado = get_object_or_404(
        ResultadoExame, id=resultado_id,
        paciente__medico=request.user
    )
    medicoes = resultado.medicoes.all()
    alertas = medicoes.exclude(status='normal')

    return render(request, 'exames/ver_resultado.html', {
        'resultado': resultado,
        'medicoes': medicoes,
        'alertas': alertas,
    })
