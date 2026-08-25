from celery import shared_task
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def enviar_lembrete_whatsapp(consulta_id):
    """Envia lembrete de consulta via WhatsApp 2h antes. Requer broker Celery configurado."""
    from .models import Consulta
    from .views import CriarAgendamentoView

    consulta = Consulta.objects.filter(id=consulta_id).first()
    if not consulta:
        logger.warning("Consulta %s não encontrada para envio de lembrete.", consulta_id)
        return

    if consulta.status != "confirmado":
        return

    mensagem = (
        f"*⏰ Lembrete de Consulta - Medicos Innosoft*\n\n"
        f"Olá {consulta.paciente.nome},\n\n"
        f"Você tem uma consulta em *2 horas*:\n"
        f"⏰ {consulta.data_hora.strftime('%H:%M')}\n"
        f"👨⚕️ {consulta.profissional.get_full_name()}\n\n"
        f"📍 Local: [Endereço da Clínica]\n"
        f"📞 Contato: [Telefone de Emergência]"
    )

    CriarAgendamentoView().enviar_whatsapp(
        telefone=f"55{consulta.paciente.telefone}",
        mensagem=mensagem,
    )
