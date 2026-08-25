from django.db import models


class Exame(models.Model):
    """Catálogo global de exames disponíveis para pedido."""
    CATEGORIAS = (
        ('laboratorial', 'Laboratorial'),
        ('imagem', 'Imagem'),
        ('procedimento', 'Procedimento'),
        ('outro', 'Outro'),
    )

    nome = models.CharField(max_length=150, unique=True)
    codigo_tuss = models.CharField(max_length=20, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default='laboratorial')
    preparo = models.TextField(blank=True, help_text="Orientações de preparo para o paciente")
    uso_count = models.PositiveIntegerField(default=0, help_text="Quantas vezes foi pedido (favoritos)")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uso_count', 'nome']
        verbose_name_plural = 'Exames'

    def __str__(self):
        return self.nome


class ValorReferencia(models.Model):
    """
    Analito com faixa de referência, usado na leitura automática dos PDFs de resultado.
    `padrao_busca` é a expressão regular usada para localizar o valor no texto do PDF
    (ex.: r'Hemoglobina\\s*[:=]?\\s*([0-9]+[.,][0-9]+)').
    """
    GENEROS = (('ambos', 'Ambos'), ('M', 'Masculino'), ('F', 'Feminino'))

    exame = models.ForeignKey(Exame, on_delete=models.CASCADE, related_name='referencias')
    analito = models.CharField(max_length=100, help_text="Ex.: Hemoglobina, Glicemia")
    padrao_busca = models.CharField(max_length=300, help_text="Regex que captura o valor no PDF (grupo 1 = número)")
    unidade = models.CharField(max_length=30, blank=True)
    valor_min = models.FloatField(null=True, blank=True)
    valor_max = models.FloatField(null=True, blank=True)
    genero = models.CharField(max_length=5, choices=GENEROS, default='ambos')
    orientacao_alto = models.CharField(max_length=250, blank=True)
    orientacao_baixo = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name_plural = 'Valores de referência'

    def __str__(self):
        return f"{self.analito} ({self.exame.nome})"


class PedidoExame(models.Model):
    evolucao = models.ForeignKey('evolucoes.Evolucao', on_delete=models.CASCADE, related_name='pedidos_exames')
    medico = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    justificativa_clinica = models.TextField(blank=True)
    origem_sugestao = models.BooleanField(default=False, help_text="Gerado a partir do motor de sugestões")
    data_pedido = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-data_pedido']

    def __str__(self):
        return f"Pedido {self.id} - {self.evolucao.paciente.nome}"

    def resumo_exames(self):
        return ", ".join(i.exame.nome for i in self.itens.all())


class ItemPedidoExame(models.Model):
    pedido = models.ForeignKey(PedidoExame, on_delete=models.CASCADE, related_name='itens')
    exame = models.ForeignKey(Exame, on_delete=models.PROTECT)
    instrucoes = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('pedido', 'exame')

    def __str__(self):
        return f"{self.exame.nome} ({self.pedido_id})"


class ResultadoExame(models.Model):
    """PDF/imagem de resultado anexado pelo médico, com leitura automática quando possível."""
    TIPOS = (('pdf', 'PDF'), ('imagem', 'Imagem'), ('outro', 'Outro'))

    paciente = models.ForeignKey('prontuario.Pacientes', on_delete=models.CASCADE, related_name='resultados_exames')
    item_pedido = models.ForeignKey(ItemPedidoExame, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=150)
    arquivo = models.FileField(upload_to='resultados/%Y/%m/%d/')
    tipo = models.CharField(max_length=10, choices=TIPOS, default='pdf')
    texto_extraido = models.TextField(blank=True)
    leitura_ok = models.BooleanField(default=False, help_text="Texto extraído e valores interpretados")
    resumo_leitura = models.TextField(blank=True, help_text="Resumo gerado automaticamente")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo

    @property
    def tem_alertas(self):
        return self.medicoes.exclude(status='normal').exists()


class MedicaoResultado(models.Model):
    STATUS = (
        ('normal', 'Normal'),
        ('alto', 'Alto'),
        ('baixo', 'Baixo'),
        ('nao_avaliado', 'Sem referência'),
    )

    resultado = models.ForeignKey(ResultadoExame, on_delete=models.CASCADE, related_name='medicoes')
    analito = models.CharField(max_length=100)
    valor = models.CharField(max_length=50)
    unidade = models.CharField(max_length=30, blank=True)
    referencia_min = models.FloatField(null=True, blank=True)
    referencia_max = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='nao_avaliado')
    orientacao = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name_plural = 'Medições do resultado'

    def __str__(self):
        return f"{self.analito}: {self.valor} {self.unidade}"
