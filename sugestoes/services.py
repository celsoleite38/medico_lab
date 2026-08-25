"""
Motor de sugestões clínicas assistidas.

Fluxo:
  1. Médico seleciona sintomas de um paciente.
  2. O sistema soma os pesos SintomaCondicao→Condicao e devolve
     as condições mais prováveis, com lista de exames e medicamentos sugeridos.
  3. Médico ajusta, escolhe uma condição e finaliza.
  4. O feedback (o que foi aceito/rejeitado) ajusta os pesos para futuras consultas.
"""
import math
from django.db.models import Sum, F
from .models import (
    Sintoma, Condicao, SintomaCondicao,
    CondicaoExameSugerida, CondicaoMedicamentoSugerido,
    AnaliseClinica, AnaliseSintoma,
)


def sugerir_causas(sintoma_ids):
    """
    Dada uma lista de IDs de sintomas, retorna lista de dicts ordenada
    por relevância:
      [{condicao, peso_total, qtd_match, qtd_total, sugestoes_exames, sugestoes_meds}]
    """
    if not sintoma_ids:
        return []

    n_informados = len(sintoma_ids)

    # Soma dos pesos das condições que casam com ao menos um sintoma
    agg = (
        SintomaCondicao.objects
        .filter(sintoma_id__in=sintoma_ids)
        .values('condicao')
        .annotate(peso_total=Sum('peso'), qtd_match=Sum(F('peso')))  # qtd_match = count via peso
    )

    resultados = []
    condicoes_totais = SintomaCondicao.objects.values_list('condicao_id', flat=True).distinct()

    for item in agg:
        cid = item['condicao']
        peso_total = item['peso_total']
        qtd_match = SintomaCondicao.objects.filter(
            condicao_id=cid, sintoma_id__in=sintoma_ids
        ).count()
        qtd_total = SintomaCondicao.objects.filter(condicao_id=cid).count()

        # Normaliza: cobertura dos sintomas × intensidade dos pesos
        cobertura = qtd_match / max(qtd_total, 1)
        intensidade = peso_total / math.sqrt(qtd_total or 1)
        score = cobertura * intensidade

        resultados.append({
            'condicao': cid,
            'peso_total': round(peso_total, 2),
            'qtd_match': qtd_match,
            'qtd_total': qtd_total,
            'score': round(score, 3),
        })

    resultados.sort(key=lambda x: x['score'], reverse=True)

    # Enriquecer com nomes e sugestões
    condicoes_ids = [r['condicao'] for r in resultados]
    mapa_condicoes = {
        c.id: c for c in Condicao.objects.filter(id__in=condicoes_ids)
    }

    exames_map = {}
    for ex in CondicaoExameSugerida.objects.filter(condicao_id__in=condicoes_ids).select_related('exame'):
        exames_map.setdefault(ex.condicao_id, []).append({
            'exame_id': ex.exame_id,
            'exame_nome': ex.exame.nome,
            'peso': ex.peso,
        })

    meds_map = {}
    for m in CondicaoMedicamentoSugerido.objects.filter(condicao_id__in=condicoes_ids).select_related('medicamento'):
        meds_map.setdefault(m.condicao_id, []).append({
            'med_id': m.medicamento_id,
            'med_nome': m.medicamento.nome,
            'peso': m.peso,
            'posologia_sugerida': m.posologia_sugerida,
        })

    for r in resultados:
        cid = r['condicao']
        r['condicao_obj'] = mapa_condicoes.get(cid)
        r['sugestoes_exames'] = sorted(exames_map.get(cid, []), key=lambda x: -x['peso'])
        r['sugestoes_meds'] = sorted(meds_map.get(cid, []), key=lambda x: -x['peso'])

    return resultados


def registrar_feedback(analise, condicao_escolhida_id, aceitou_sugestao):
    """
    Ajusta pesos da base de conhecimento com base no que o médico escolheu.
    - Para a condição escolhida: aumenta o peso dos sintomas que nela constam.
    - Para condições não escolhidas que apareceram: diminui levemente os pesos.
    Atualiza uso_count dos exames e medicamentos incluídos no pedido/receita.
    """
    if condicao_escolhida_id:
        analise.condicao_escolhida_id = condicao_escolhida_id
        analise.aceitou_sugestao = aceitou_sugestao
        analise.save()

        # Boost: aumenta peso da condição escolhida para os sintomas informados
        for item in analise.analisesintoma_set.filter(confirmado=True):
            SintomaCondicao.objects.filter(
                sintoma=item.sintoma, condicao_id=condicao_escolhida_id
            ).update(peso=Min(F('peso') * 1.2, 5.0))

        # Decay levemente nas condições não escolhidas que tinham algum overlap
        ids_nao_escolhidos = SintomaCondicao.objects.filter(
            sintoma__in=[i.sintoma_id for i in analise.analisesintoma_set.filter(confirmado=True)]
        ).exclude(condicao_id=condicao_escolhida_id).values_list('condicao_id', flat=True).distinct()

        for cid in ids_nao_escolhidos:
            SintomaCondicao.objects.filter(
                condicao_id=cid,
                sintoma__in=[i.sintoma_id for i in analise.analisesintoma_set.filter(confirmado=True)]
            ).update(peso=Max(F('peso') * 0.95, 0.05))

    return analise


def incrementar_uso_exames(item_pedido_ids):
    """Incrementa uso_count dos exames incluídos em pedidos gerados por sugestões."""
    from exames.models import ItemPedidoExame
    from django.db.models import F
    ItemPedidoExame.objects.filter(id__in=item_pedido_ids).select_related('exame').update(
        exame__uso_count=F('exame__uso_count') + 1
    )


def incrementar_uso_medicamentos(receita_item_ids):
    """Incrementa uso_count dos medicamentos incluídos em receitas geradas por sugestões."""
    from receituario.models import ReceitaItem
    from django.db.models import F
    ReceitaItem.objects.filter(id__in=receita_item_ids).select_related('medicamento').update(
        medicamento__uso_count=F('medicamento__uso_count') + 1
    )


# Django F() expressions don't have aggregate functions, so do the cap manually
from django.db.models import Min, Max, F
