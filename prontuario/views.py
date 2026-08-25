from collections import defaultdict
import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from django.template.loader import render_to_string
from weasyprint import HTML
from autenticacao.models import PerfilProfissional
from evolucoes.models import Evolucao
from .models import Pacientes, DadosPaciente
from datetime import date, datetime
from .forms import PacienteForm

logger = logging.getLogger(__name__)


@login_required(login_url='/auth/logar/')
def pacientes(request):
    
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(medico=request.user)
        
        query = request.GET.get('q')
        
        if query:
            pacientes = pacientes.filter(nome__icontains=query)
                    
        return render(request, 'pacientes.html', {
            'pacientes': pacientes,
            'query': query
        })
        
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        sexo = request.POST.get('sexo')
        estadocivil = request.POST.get('estadocivil')
        datanascimento = request.POST.get('datanascimento')
        naturalidade = request.POST.get('naturalidade')
        profissao = request.POST.get('profissao')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        
        # CORREÇÃO: Removi a referência ao 'id' que não existe
        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(cpf.strip()) == 0) or (len(estadocivil.strip()) == 0) or (len(datanascimento.strip()) == 0) or (len(naturalidade.strip()) == 0) or (len(profissao.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0) or (len(endereco.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('prontuario:pacientes')  # ← CORREÇÃO: volta para a lista
        
        pacientes = Pacientes.objects.filter(email=email)
        
        if pacientes.exists():     
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('prontuario:pacientes')  # ← CORREÇÃO: volta para a lista
        
        try: 
            p1 = Pacientes(
                nome=nome,
                cpf=cpf,
                sexo=sexo,
                estadocivil=estadocivil,
                datanascimento=datanascimento,
                naturalidade=naturalidade,
                profissao=profissao,
                email=email,
                telefone=telefone,
                endereco=endereco,
                medico=request.user
            )
            
            p1.save()
        
            messages.add_message(request, constants.SUCCESS, 'Paciente Cadastrado com Sucesso')
            # CORREÇÃO: Redireciona para a lista de pacientes ou para o novo paciente
            return redirect('prontuario:dados_paciente', id=p1.id)  # ← Volta para a lista
           
    
        except Exception:
            logger.exception("Erro ao salvar paciente")
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('prontuario:pacientes')  # ← CORREÇÃO: volta para a lista
    
@login_required(login_url='/auth/logar/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(medico=request.user)
        query = request.GET.get('q')
        if query:
            pacientes = pacientes.filter(nome__icontains=query)
        
        return render(request, 'dados_paciente_listar.html', {
            'pacientes': pacientes,
            'query': query
        })
        
    
@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.medico == request.user:
        messages.add_message(request, constants.ERROR, 'Acesso negado a este PACIENTE.')
        return redirect('prontuario:dados_paciente_listar')
    
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    
    elif request.method == "POST":
        peso = request.POST.get('peso')
        qp = request.POST.get('qp')
        hma = request.POST.get('hma')
        hpp = request.POST.get('hpp')
        antecedentepf = request.POST.get('antecedentepf')
        exame_fisico = request.POST.get('exame_fisico')
        exames_complementares = request.POST.get('exames_complementares')
        diagnostico = request.POST.get('diagnostico')
        plano_terapeutico = request.POST.get('plano_terapeutico')
        data_dadospaciente = request.POST.get('data_dadospaciente') or datetime.date.today()
        
        # Validação para garantir que todos os campos estejam preenchidos
        if (len(peso.strip()) == 0) or (len(qp.strip()) == 0) or (len(hma.strip()) == 0) or (len(hpp.strip()) == 0) or (len(antecedentepf.strip()) == 0) or (len(exame_fisico.strip()) == 0) or (len(exames_complementares.strip()) == 0) or (len(diagnostico.strip()) == 0) or (len(plano_terapeutico.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos, use 0 ou - quando nao houver valor!')
            return redirect('prontuario:dados_paciente', id=id)
        
        dados = DadosPaciente(
            paciente=paciente,
            peso=peso,
            qp=qp,
            hma=hma,
            hpp=hpp,
            antecedentepf=antecedentepf,
            exame_fisico=exame_fisico,
            exames_complementares=exames_complementares,
            diagnostico=diagnostico,
            plano_terapeutico=plano_terapeutico,
            data_dadospaciente=data_dadospaciente
        )
        dados.save()
        
        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
        return redirect(f'/prontuario/dados_paciente/{id}/')

    



@login_required(login_url='/auth/logar/')
def editar_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.medico == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/prontuario/pacientes/')
    if request.method == "POST":
        paciente.nome = request.POST.get('nome')
        paciente.cpf = request.POST.get('cpf')
        paciente.sexo = request.POST.get('sexo')
        paciente.estadocivil = request.POST.get('estadocivil')
        paciente.datanascimento = request.POST.get('datanascimento')
        paciente.naturalidade = request.POST.get('naturalidade')
        paciente.profissao = request.POST.get('profissao')
        paciente.email = request.POST.get('email')
        paciente.telefone = request.POST.get('telefone')
        paciente.endereco = request.POST.get('endereco')
        
        if any(len(campo.strip()) == 0 for campo in [
            paciente.nome, paciente.sexo, paciente.estadocivil, paciente.datanascimento,
            paciente.naturalidade, paciente.profissao, paciente.email, paciente.telefone,
            paciente.endereco
        ]):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect(f'/prontuario/editar_paciente/{id}/')

        try:
            paciente.datanascimento = datetime.strptime(paciente.datanascimento, '%Y-%m-%d').date()
            paciente.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente atualizado com sucesso!')
            return redirect('/prontuario/pacientes/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao atualizar paciente')
            messages.add_message(request, constants.ERROR, 'Data de nascimento inválida')
            return redirect(f'/prontuario/editar_paciente/{id}/')

    return render(request, 'editar_paciente.html', {'paciente': paciente})
            
            
@login_required(login_url='/auth/logar/')
def plano_evolucao_listar (request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(medico=request.user)
        query = request.GET.get('q')
        if query:
            pacientes = pacientes.filter(nome__icontains=query)
        
        return render(request, 'plano_evolucao_listar.html', {
            'pacientes': pacientes,
            'query': query
        })
        
    
        
@login_required(login_url='/auth/logar/')
def plano_evolucao(request, id):
    paciente = get_object_or_404(Pacientes, id=id, medico=request.user)
    
    evolucoes = Evolucao.objects.filter(paciente=paciente).order_by("data_criacao")

    evolucoes_por_data = defaultdict(list)
    for evolucao in evolucoes:
        evolucoes_por_data[evolucao.data_criacao].append(evolucao)
    
    

    
    if request.method == "GET":
        r1 = Evolucao.objects.filter(paciente=paciente).order_by("data_criacao")
        o1 = Evolucao.objects.filter(paciente=paciente).values_list('evolucao', flat=True)
        #return render(request, 'plano_evolucao.html', {'paciente': paciente, 'evolucao': r1, 'evolucao': o1})
    
        return render(request, 'plano_evolucao.html', {'paciente': paciente,  'evolucao': r1, 'evolucoes':evolucoes, })

@login_required(login_url='/auth/logar/')
def evolucao(request, id):  # id = id do paciente
    paciente = get_object_or_404(Pacientes, id=id)
    
    if not paciente.medico == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/prontuario/dados_evolucao/')  # ajuste se necessário
    
    if request.method == "POST":
        titulo = request.POST.get('titulo', '').strip()
        evolucao_texto = request.POST.get('evolucao', '').strip()
        data_str = request.POST.get('data_criacao', '').strip()  # string do input date
        
        # Validação básica
        if not titulo or not evolucao_texto:
            messages.add_message(request, constants.ERROR, 'Preencha título e evolução obrigatoriamente!')
            return redirect('prontuario:evolucao', id=id)
        
        # Tratamento da data de forma segura
        if data_str:
            try:
                # Converte a string 'YYYY-MM-DD' para objeto date
                data_criacao = datetime.strptime(data_str, '%Y-%m-%d').date()
            except ValueError:
                # Se o formato estiver errado (ex.: usuário digitou algo inválido)
                data_criacao = date.today()
                messages.add_message(request, constants.WARNING, 'Data inválida. Usando a data de hoje.')
        else:
            # Campo vazio → usa data atual
            data_criacao = date.today()
            messages.add_message(request, constants.INFO, 'Data não informada. Usando data atual.')
        
        # Cria a evolução
        nova_evolucao = Evolucao(
            paciente=paciente,
            titulo=titulo,
            evolucao=evolucao_texto,
            data_criacao=data_criacao,
            # imagem = request.FILES.get('imagem')   ← descomente se quiser tratar imagem
        )
        
        nova_evolucao.save()
        
        messages.add_message(request, constants.SUCCESS, 'Evolução cadastrada com sucesso!')
        return redirect('prontuario:plano_evolucao', id=id)
    
    # Se for GET (não deve acontecer, pois vem do modal POST)
    # Mas para segurança, redireciona ou renderiza algo
    return redirect('prontuario:plano_evolucao', id=id)



@login_required(login_url='/auth/logar/')
def imprimir_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id, medico=request.user)

    html_string = render_to_string('imprimir_paciente_pdf.html', {
        'paciente': paciente,
        'today': date.today(),
    })
    pdf = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{paciente.nome}.pdf"'
    return response


#impressao de relatorio - evoluções
@login_required(login_url='/auth/logar/')
def imprimir_evolucoes(request, paciente_id):
    paciente = get_object_or_404(Pacientes, id=paciente_id, medico=request.user)
    perfil = PerfilProfissional.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        ids_selecionados = request.POST.getlist('evolucoes')

        if ids_selecionados:
            # Filtra SEMPRE pelo paciente do médico logado (evita acesso a evoluções de outros pacientes)
            evolucoes = Evolucao.objects.filter(id__in=ids_selecionados, paciente=paciente)
        else:
            evolucoes = Evolucao.objects.filter(paciente=paciente)

        return render(request, 'relatorio_impressao.html', {
            'paciente': paciente,
            'evolucoes': evolucoes,
            'today': date.today(),
            'perfil': perfil
        })

    else:
        evolucoes = Evolucao.objects.filter(paciente=paciente)
        return render(request, 'selecionar_evolucoes.html', {
            'paciente': paciente,
            'evolucoes': evolucoes
        })


@login_required(login_url='/auth/logar/')
def imprimir_dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id, medico=request.user)

    dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
    if request.method == 'POST':
        # Não há nada a fazer aqui, pois não estamos lidando com formulários
        pass
    else:
        return render(request, 'imprimir_dados_paciente.html', {
            'paciente': paciente,
            'dados_paciente': dados_paciente,
            'today': date.today()
        })

