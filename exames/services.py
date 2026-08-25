"""
Leitor e intérprete de resultados de exames em PDF.

Fluxo:
  1. Extrai texto do PDF via pypdf.
  2. Para cada ValorReferencia ativo, usa a regex `padrao_busca` para
     encontrar o valor numérico no texto extraído.
  3. Compara com faixa de referência e classifica como normal/alto/baixo.
  4. Retorna lista de medições encontradas + resumo para o médico.
"""
import re
import logging

logger = logging.getLogger(__name__)


def extrair_texto_pdf(caminho_arquivo):
    """Extrai todo o texto de um PDF. Retorna string vazia se falhar."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(caminho_arquivo)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() or ""
        return texto
    except Exception as e:
        logger.warning("Não foi possível extrair texto do PDF %s: %s", caminho_arquivo, e)
        return ""


def interpretar_resultado(texto):
    """
    Compara o texto do PDF contra todas as ValorReferencia ativas.
    Retorna dict com:
      - medicoes: lista de dicts {analito, valor, unidade, min, max, status, orientacao}
      - resumo: texto resumido pronto para exibição
      - alertas: lista dos itens com status != 'normal'
    """
    from exames.models import ValorReferencia
    import re

    medicoes = []
    alertas = []

    for vr in ValorReferencia.objects.filter(exame__ativo=True):
        try:
            match = re.search(vr.padrao_busca, texto, re.IGNORECASE | re.DOTALL)
        except re.error:
            continue

        if not match:
            continue

        # Grupo 1 deve conter o número
        valor_str = match.group(1).replace(',', '.').strip()
        try:
            valor_num = float(valor_str)
        except ValueError:
            continue

        # Classificar
        status = 'normal'
        orientacao = ''

        if vr.valor_min is not None and valor_num < vr.valor_min:
            status = 'baixo'
            orientacao = vr.orientacao_baixo or f"Valor abaixo de {vr.valor_min}"
        elif vr.valor_max is not None and valor_num > vr.valor_max:
            status = 'alto'
            orientacao = vr.orientacao_alto or f"Valor acima de {vr.valor_max}"

        medicao = {
            'analito': vr.analito,
            'valor': valor_str,
            'valor_num': valor_num,
            'unidade': vr.unidade,
            'min': vr.valor_min,
            'max': vr.valor_max,
            'status': status,
            'orientacao': orientacao,
        }
        medicoes.append(medicao)

        if status != 'normal':
            alertas.append(medicao)

    # Gerar resumo
    linhas = []
    for m in medicoes:
        icone = {'normal': '✅', 'alto': '🔺', 'baixo': '🔻'}.get(m['status'], '❓')
        ref = ""
        if m['min'] is not None or m['max'] is not None:
            ref_min = m['min'] if m['min'] is not None else '-'
            ref_max = m['max'] if m['max'] is not None else '-'
            ref = f" (ref: {ref_min}–{ref_max} {m['unidade']})"
        linhas.append(f"{icone} {m['analito']}: {m['valor']} {m['unidade']}{ref}")

    if alertas:
        linhas.append("")
        linhas.append(f"⚠ {len(alertas)} valor(es) fora da faixa de referência:")
        for a in alertas:
            linhas.append(f"  • {a['analito']}: {a['orientacao']}")

    resumo = "\n".join(linhas) if linhas else "Nenhum valor de referência identificado no PDF."

    return {
        'medicoes': medicoes,
        'alertas': alertas,
        'resumo': resumo,
    }
