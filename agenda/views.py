from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, TemplateView, UpdateView
from .models import Consulta
from .forms import AgendamentoForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required # Para a função de cancelamento
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_POST # Para garantir que o cancelamento seja POST
from datetime import datetime, timedelta
import json
import logging
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# Função auxiliar unificada para obter a cor do status
def get_cor_status(status):
    cores = {
        "agendado": "#3498db",
        "confirmado": "#2ecc71",
        "cancelado": "#e74c3c",
        "realizado": "#9b59b6"
    }
    return cores.get(status, "#3498db")

class CriarAgendamentoView(LoginRequiredMixin, CreateView):
    model = Consulta
    form_class = AgendamentoForm
    template_name = "agenda/criar_agendamento.html"
    success_url = reverse_lazy("agenda:calendario")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.profissional = self.request.user
        response = super().form_valid(form)

        # ================================================
        # 1. ENVIO IMEDIATO VIA WHATSAPP (opcional)
        # Só envia se WHATSAPP_TOKEN e WHATSAPP_BUSINESS_ID estiverem configurados.
        # ================================================
        paciente = form.instance.paciente
        data_formatada = form.instance.data_hora.strftime("%d/%m/%Y às %H:%M")

        mensagem_confirmacao = (
            f"*📅 Confirmação de Agendamento - Medicos Innosoft*\n\n"
            f"Olá {paciente.nome},\n\n"
            f"✅ *Consulta agendada com sucesso!*\n"
            f"👨⚕️ Profissional: {form.instance.profissional.get_full_name()}\n"
            f"📆 Data/Hora: {data_formatada}\n"
            f"⏳ Duração: {form.instance.duracao} minutos\n\n"
            f"📍 Local: [Endereço da Clínica]\n\n"

        )

        self.enviar_whatsapp(
            telefone=f"55{paciente.telefone}",
            mensagem=mensagem_confirmacao
        )

        # ================================================
        # 2. AGENDAMENTO DO LEMBRETE (2H ANTES) — opcional, exige broker Celery configurado
        # ================================================
        hora_lembrete = form.instance.data_hora - timedelta(hours=2)
        try:
            from .tasks import enviar_lembrete_whatsapp
            enviar_lembrete_whatsapp.apply_async(
                args=[form.instance.id],
                eta=hora_lembrete
            )
        except Exception as e:
            # Sem broker Celery configurado, o agendamento continua funcionando sem lembrete
            logger.warning("Não foi possível agendar lembrete para consulta %s: %s", form.instance.id, e)

        return response

    def enviar_whatsapp(self, telefone, mensagem):
        """Envia mensagem via WhatsApp Business API. Não gera erro se não estiver configurado."""
        business_id = getattr(settings, 'WHATSAPP_BUSINESS_ID', None)
        token = getattr(settings, 'WHATSAPP_TOKEN', None)
        if not business_id or not token:
            logger.info("WhatsApp não configurado (WHATSAPP_TOKEN/WHATSAPP_BUSINESS_ID). Mensagem não enviada.")
            return

        try:
            import requests
        except ImportError:
            logger.warning("Biblioteca 'requests' não instalada. Mensagem WhatsApp não enviada.")
            return

        url = f"https://graph.facebook.com/v18.0/{business_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": telefone,
            "type": "text",
            "text": {"body": mensagem}
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code != 200:
                logger.error("Erro WhatsApp: %s", response.text)
        except Exception as e:
            logger.error("Falha na API WhatsApp: %s", e)

# ================================================
# TAREFA CELERY PARA LEMBRETE (RODA 2H ANTES) — movida para agenda/tasks.py
# ================================================

class EditarConsultaView(LoginRequiredMixin, UpdateView):
    model = Consulta
    form_class = AgendamentoForm
    template_name = "agenda/editar_consulta.html"

    def get_success_url(self):
        return reverse_lazy("agenda:detalhes_consulta", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return Consulta.objects.filter(profissional=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

@login_required
@require_POST # Garante que esta view só aceite requisições POST
def cancelar_consulta_view(request, pk):
    try:
        consulta = get_object_or_404(Consulta, pk=pk)

        # Verifica se o usuário logado é o profissional da consulta
        if consulta.profissional != request.user:
            return JsonResponse({"success": False, "message": "Você não tem permissão para cancelar esta consulta."}, status=403)
        
        # Verifica se a consulta já está cancelada ou realizada
        if consulta.status == "cancelado":
            return JsonResponse({"success": False, "message": "Esta consulta já está cancelada."}, status=400)
        if consulta.status == "realizado":
            return JsonResponse({"success": False, "message": "Não é possível cancelar uma consulta já realizada."}, status=400)

        consulta.status = "cancelado" # Define o status como cancelado
        consulta.save()
        return JsonResponse({"success": True, "message": "Consulta cancelada com sucesso!"})

    except Consulta.DoesNotExist:
        return JsonResponse({"success": False, "message": "Consulta não encontrada."}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": f"Ocorreu um erro: {str(e)}"}, status=500)
# Fim da função cancelar_consulta_view - Certifique-se de que a próxima função está corretamente desindentada.

@login_required
def detalhes_consulta(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk, profissional=request.user)
    return render(request, "agenda/detalhes_consulta.html", {"consulta": consulta})

class CalendarioView(LoginRequiredMixin, TemplateView):
    template_name = "agenda/calendario.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@login_required
def consultas_json(request):
    consultas = Consulta.objects.filter(profissional=request.user)
    eventos = []
    for consulta in consultas:
        eventos.append({
            "id": consulta.id,
            "title": f"{consulta.paciente.nome} ({consulta.get_status_display()})",
            "start": consulta.data_hora.isoformat(),
            "end": (consulta.data_hora + timedelta(minutes=consulta.duracao)).isoformat(),
            "color": get_cor_status(consulta.status),
            "extendedProps": {
                "paciente_id": consulta.paciente.id,
                "telefone": consulta.paciente.telefone,
                "observacoes": consulta.observacoes,
                "status": consulta.status
            }
        })
    return JsonResponse(eventos, safe=False)

class RelatorioView(LoginRequiredMixin, TemplateView):
    template_name = 'agenda/relatorio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inicio_semana = datetime.now() - timedelta(days=7)
        consultas = Consulta.objects.filter(
            profissional=self.request.user,
            data_hora__gte=inicio_semana
        )
        context['stats'] = {
            'total': consultas.count(),
            'confirmados': consultas.filter(status='confirmado').count(),
            'cancelados': consultas.filter(status='cancelado').count(),
            'ocupacao': (consultas.filter(status='confirmado').count() / consultas.count() * 100) if consultas.count() > 0 else 0,
        }
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('agenda/_relatorio_parcial.html', context, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


@login_required
def relatorio_parcial(request):
    inicio_semana = datetime.now() - timedelta(days=7)
    consultas = Consulta.objects.filter(profissional=request.user, data_hora__gte=inicio_semana)

    context = {
        'stats': {
            'total': consultas.count(),
            'confirmados': consultas.filter(status='confirmado').count(),
            'cancelados': consultas.filter(status='cancelado').count(),
            'ocupacao': (consultas.filter(status='confirmado').count() / consultas.count() * 100) if consultas.count() > 0 else 0,
        }
    }
    html = render_to_string('agenda/_relatorio_parcial.html', context)
    return JsonResponse({'html': html})
