from datetime import timedelta
import json
import logging

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Assinatura
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

try:
    import mercadopago
except ImportError:  # biblioteca opcional em desenvolvimento
    mercadopago = None

logger = logging.getLogger(__name__)


def _mercadopago_disponivel():
    if mercadopago is None:
        logger.error("Biblioteca 'mercadopago' não instalada. Rode: pip install mercadopago")
        return False
    if not getattr(settings, 'MERCADO_PAGO_ACCESS_TOKEN', ''):
        logger.error("MERCADO_PAGO_ACCESS_TOKEN não configurado.")
        return False
    return True


def pagina_vendas(request):
   
    planos = [
        {"nome": "Plano Mensal", "duracao": "1 mês", "preco": "R$ 29,90", "link": "/pagamento/1-mes/"},
        {"nome": "Plano Trimestral", "duracao": "3 meses", "preco": "R$ 79,90", "link": "/pagamento/3-meses/"},
        {"nome": "Plano Semestral", "duracao": "6 meses", "preco": "R$ 149,90", "link": "/pagamento/6-meses/"},
        {"nome": "Teste Gratuito", "duracao": "7 dias", "preco": "Grátis", "link": "/teste-gratis/"},
    ]
    return render(request, 'paginas_vendas/pagina_vendas.html', {'planos': planos})

def teste_gratis(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if Assinatura.objects.filter(email=email, eh_teste_gratis=True).exists():
            return render(request, 'paginas_vendas/erro.html', {
                'mensagem': 'Este e-mail já utilizou o teste gratuito.',
                'email': email
            })

        validade = timezone.now() + timedelta(days=7)

        Assinatura.objects.create(
            email=email,
            plano="Teste Grátis (7 dias)",
            valor=0,
            validade=validade,
            status="teste",
            eh_teste_gratis=True
        )

        # ATENÇÃO: aqui precisa passar 'validade' como contexto
        return render(request, 'paginas_vendas/teste_gratis_sucesso.html', {
            'validade': validade
        })

    return render(request, 'paginas_vendas/teste_gratis_form.html')

 

def checkout(request, plano_slug):
    planos = {
        "1-mes": {"title": "Plano Mensal", "price": 29.90},
        "3-meses": {"title": "Plano Trimestral", "price": 79.90},
        "6-meses": {"title": "Plano Semestral", "price": 149.90},
    }

    plano = planos.get(plano_slug)
    if not plano:
        return redirect('pagina_vendas')

    if not _mercadopago_disponivel():
        return render(request, 'paginas_vendas/erro.html', {
            'mensagem': 'Pagamentos temporariamente indisponíveis. Tente novamente mais tarde.'
        })

    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    preference_data = {
        "items": [
            {
                "title": plano["title"],
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": plano["price"],
            }
        ],
        "back_urls": {
            "success": request.build_absolute_uri('/obrigado/'),
            "failure": request.build_absolute_uri('/'),
        },
        "auto_return": "approved"
    }
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    return redirect(preference["init_point"])

def pagina_obrigado(request):
    return render(request, 'paginas_vendas/obrigado.html')




@csrf_exempt
def webhook_mercadopago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if data.get("type") == "payment":
                payment_id = data.get("data", {}).get("id")

                if not _mercadopago_disponivel():
                    return JsonResponse({"error": "Pagamentos não configurados"}, status=503)

                sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
                payment = sdk.payment().get(payment_id)["response"]

                if payment["status"] == "approved":
                    # Evita criar assinatura duplicada quando o Mercado Pago reenvia a notificação
                    ja_registrada = Assinatura.objects.filter(
                        email=payment["payer"]["email"],
                        plano=payment["additional_info"]["items"][0]["title"],
                        status="ativo",
                        validade__gte=timezone.now(),
                    ).exists()
                    if not ja_registrada:
                        email = payment["payer"]["email"]
                        valor = payment["transaction_amount"]
                        plano_nome = payment["additional_info"]["items"][0]["title"]

                        dias = {
                            "Plano Mensal": 30,
                            "Plano Trimestral": 90,
                            "Plano Semestral": 180
                        }
                        validade = timezone.now() + timedelta(days=dias.get(plano_nome, 30))

                        Assinatura.objects.create(
                            email=email,
                            plano=plano_nome,
                            valor=valor,
                            validade=validade,
                            status="ativo"
                        )

            return JsonResponse({"status": "received"})

        except Exception:
            logger.exception("Erro no webhook do Mercado Pago")
            return JsonResponse({"error": "Erro interno"}, status=500)

    # Caso não seja POST, retorna erro
    return JsonResponse({"error": "Método não permitido"}, status=405)



@staff_member_required
def dashboard_assinaturas(request):
    assinaturas = Assinatura.objects.all().order_by('-data_pagamento')
    return render(request, 'paginas_vendas/dashboard.html', {'assinaturas': assinaturas})


def recursos(request):
    return render(request, 'paginas_vendas/recursos.html')