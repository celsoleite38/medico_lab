from django.http import HttpResponse
def teste(request):
    return HttpResponse("App documentos funcionando!")
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from evolucoes.models import Evolucao
from .models import Receituario
from .forms import AtestadoForm, ExameAnexadoForm, PedidoExameForm, ReceituarioForm, ReceituarioItemFormSet
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import date


@login_required
def adicionar_receituario(request, evolucao_id):
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    
    if request.method == 'POST':
        form = ReceituarioForm(request.POST)
        formset = ReceituarioItemFormSet(request.POST, instance=Receituario(evolucao=evolucao, medico=request.user))
        if form.is_valid() and formset.is_valid():
            receituario = form.save(commit=False)
            receituario.evolucao = evolucao
            receituario.medico = request.user
            receituario.save()
            formset.instance = receituario
            formset.save()
            messages.add_message(request, constants.SUCCESS, 'Receituário adicionado com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
        else:
            messages.add_message(request, constants.ERROR, 'Verifique os dados informados.')
    else:
        form = ReceituarioForm()
    
    return render(request, 'documentos/adicionar_receituario.html', {
        'form': form,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
    })
    


@login_required
def gerar_pdf_receituario(request, receituario_id):
    receituario = get_object_or_404(Receituario, id=receituario_id, evolucao__paciente__medico=request.user)
    
    context = {
        'receituario': receituario,
        'paciente': receituario.evolucao.paciente,
        'medico': request.user,  # ou receituario.medico
        'today': date.today(),
        # adicione dados do seu PerfilProfissional se quiser
    }
    
    html_string = render_to_string('documentos/pdf_receituario.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receituario_{receituario.id}_{receituario.data_emissao}.pdf"'
    return response

@login_required
def adicionar_pedido_exame(request, evolucao_id):
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    
    if request.method == 'POST':
        form = PedidoExameForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.evolucao = evolucao
            pedido.medico = request.user
            pedido.save()
            messages.add_message(request, constants.SUCCESS, 'Pedido de exame adicionado com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
        else:
            messages.add_message(request, constants.ERROR, 'Verifique os dados informados.')
    else:
        form = PedidoExameForm()
    
    return render(request, 'documentos/adicionar_pedido_exame.html', {
        'form': form,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
    })
    
@login_required
def adicionar_atestado(request, evolucao_id):
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    
    if request.method == 'POST':
        form = AtestadoForm(request.POST)
        if form.is_valid():
            atestado = form.save(commit=False)
            atestado.evolucao = evolucao
            atestado.medico = request.user
            atestado.save()
            messages.add_message(request, constants.SUCCESS, 'Atestado adicionado com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
    else:
        form = AtestadoForm()
    
    return render(request, 'documentos/adicionar_atestado.html', {
        'form': form,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
    })
    

@login_required
def adicionar_exame_anexado(request, evolucao_id):
    evolucao = get_object_or_404(Evolucao, id=evolucao_id, paciente__medico=request.user)
    
    if request.method == 'POST':
        form = ExameAnexadoForm(request.POST, request.FILES)
        if form.is_valid():
            exame = form.save(commit=False)
            exame.evolucao = evolucao
            exame.save()
            messages.add_message(request, constants.SUCCESS, 'Exame anexado com sucesso.')
            return redirect('evolucoes:detalhe_evolucao', evolucao_id=evolucao.id)
    else:
        form = ExameAnexadoForm()
    
    return render(request, 'documentos/adicionar_exame_anexado.html', {
        'form': form,
        'evolucao': evolucao,
        'paciente': evolucao.paciente,
    })