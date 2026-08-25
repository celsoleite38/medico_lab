import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages import constants
from django.template.loader import render_to_string
from weasyprint import HTML
from datetime import date
from .models import Medicamento, Receita, ReceitaItem
from .forms import ReceitaForm, ReceitaItemFormSet
from evolucoes.models import Evolucao

logger = logging.getLogger(__name__)


@login_required
def lista_receitas(request):
    """Lista todas as receitas do médico logado."""
    receitas = Receita.objects.filter(
        medico=request.user
    ).select_related('evolucao', 'evolucao__paciente').prefetch_related('itens', 'itens__medicamento')

    q = request.GET.get('q', '').strip()
    if q:
        receitas = receitas.filter(
            Q(evolucao__paciente__nome__icontains=q) |
            Q(itens__medicamento__nome__icontains=q)
        ).distinct()

    return render(request, 'receituario/lista_receitas.html', {'receitas': receitas, 'query': q})


@login_required
def buscar_medicamentos(request):
    """Busca AJAX de medicamentos, ordenados por uso (favoritos primeiro)."""
    q = request.GET.get('q', '').strip()
    qs = Medicamento.objects.filter(ativo=True)
    if q:
        qs = qs.filter(nome__icontains=q) | qs.filter(principio_ativo__icontains=q)
    meds = qs[:20]

    data = [{
        'id': m.id,
        'nome': m.nome,
        'principio_ativo': m.principio_ativo,
        'apresentacoes': m.apresentacoes,
        'uso_count': m.uso_count,
    } for m in meds]
    return JsonResponse(data, safe=False)


@login_required
def nova_receita(request, evolucao_id=None, paciente_id=None):
    """Cria nova receita. Aceita evolucao_id ou paciente_id (usa evolução mais recente)."""
    if evolucao_id:
        evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    elif paciente_id:
        from prontuario.models import Pacientes
        paciente = get_object_or_404(Pacientes, id=paciente_id, medico=request.user)
        evolucao = Evolucao.objects.filter(paciente=paciente).order_by('-data_criacao').first()
        if not evolucao:
            messages.error(request, 'Crie pelo menos uma evolução antes de emitir receitas.')
            return redirect('prontuario:dados_paciente', id=paciente.id)
    else:
        return redirect('prontuario:pacientes')

    if request.method == 'POST':
        form = ReceitaForm(request.POST)
        formset = ReceitaItemFormSet(request.POST, prefix='itens')

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)
            receita.evolucao = evolucao
            receita.medico = request.user
            receita.save()

            formset.instance = receita
            itens = formset.save()

            # Incrementar uso_count dos medicamentos prescritos
            for item in itens:
                Medicamento.objects.filter(id=item.medicamento_id).update(
                    uso_count=item.medicamento.uso_count + 1
                )

            messages.success(request, f'Receita {receita.id} criada com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
        else:
            messages.error(request, 'Verifique os dados informados.')
    else:
        form = ReceitaForm()
        formset = ReceitaItemFormSet(prefix='itens')

    return render(request, 'receituario/nova_receita.html', {
        'form': form,
        'formset': formset,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
    })


@login_required
def receita_pdf(request, receita_id):
    receita = get_object_or_404(
        Receita, id=receita_id,
        evolucao__paciente__medico=request.user
    )
    from autenticacao.models import PerfilProfissional
    perfil = PerfilProfissional.objects.filter(usuario=request.user).first()

    html_string = render_to_string('receituario/receita_pdf.html', {
        'receita': receita,
        'perfil': perfil,
        'today': date.today(),
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receita_{receita.id}.pdf"'
    response.write(HTML(string=html_string).write_pdf())
    return response
