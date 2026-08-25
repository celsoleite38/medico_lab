from django.db import models


class Medicamento(models.Model):
    """Catálogo global de medicamentos. `uso_count` ordena os mais prescritos primeiro."""
    nome = models.CharField(max_length=150, unique=True)
    principio_ativo = models.CharField(max_length=150, blank=True)
    apresentacoes = models.TextField(blank=True, help_text="Ex.: 500mg comprimido; 20mg/mL gotas")
    uso_count = models.PositiveIntegerField(default=0, help_text="Quantas vezes foi prescrito (favoritos)")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uso_count', 'nome']
        verbose_name_plural = 'Medicamentos'

    def __str__(self):
        return self.nome


class Receita(models.Model):
    evolucao = models.ForeignKey('evolucoes.Evolucao', on_delete=models.CASCADE, related_name='receituarios')
    medico = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    observacoes_gerais = models.TextField(blank=True)
    origem_sugestao = models.BooleanField(default=False, help_text="Gerada a partir do motor de sugestões")
    data_emissao = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-data_emissao']

    def __str__(self):
        return f"Receita {self.id} - {self.evolucao.paciente.nome}"


class ReceitaItem(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='itens')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dosagem = models.CharField(max_length=100, help_text='Ex.: "20mg" ou "1 comprimido 500mg"')
    quantidade = models.CharField(max_length=50, blank=True, help_text='Ex.: "30 comprimidos"')
    posologia = models.TextField(help_text='Ex.: "1 cp de 12/12h por 7 dias"')
    observacoes_item = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.medicamento.nome} - {self.dosagem}"
