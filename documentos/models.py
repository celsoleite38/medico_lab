from django.db import models
from django.contrib.auth.models import User
from datetime import date
from evolucoes.models import Evolucao   # import do novo app


class Medicamento(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    principio_ativo = models.CharField(max_length=150, blank=True)
    apresentacoes = models.TextField(blank=True)  # ex.: "10mg cp, 20mg cp, 40mg cp"
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nome']
    
    def __str__(self):
        return self.nome


class Receituario(models.Model):
    evolucao = models.ForeignKey('evolucoes.Evolucao', on_delete=models.CASCADE, related_name='receituarios')
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_emissao = models.DateField(auto_now_add=True)
    observacoes_gerais = models.TextField(blank=True)
    
    def __str__(self):
        return f"Receituário {self.id} - {self.evolucao.paciente.nome}"

class ReceituarioItem(models.Model):
    receituario = models.ForeignKey(Receituario, on_delete=models.CASCADE, related_name='itens')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    dosagem = models.CharField(max_length=100)  # ex.: "20mg", "1 comprimido 500mg"
    quantidade = models.CharField(max_length=50, blank=True)  # ex.: "30 comprimidos"
    posologia = models.TextField()  # ex.: "1 cp 12/12h por 7 dias"
    observacoes_item = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.medicamento.nome} - {self.dosagem}"

class PedidoExame(models.Model):
    evolucao = models.ForeignKey(Evolucao, on_delete=models.CASCADE, related_name='pedidos_exames')
    exames_solicitados = models.TextField()     # ex.: "Hemograma completo\nGlicemia de jejum"
    justificativa_clinica = models.TextField(blank=True)
    data_pedido = models.DateField(default=date.today)
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Pedido Exame {self.id}"

class Atestado(models.Model):
    evolucao = models.ForeignKey(Evolucao, on_delete=models.CASCADE, related_name='atestados')
    cid = models.CharField(max_length=10, blank=True)
    descricao = models.TextField()
    periodo = models.CharField(max_length=100)  # ex.: "de 18/02/2026 a 25/02/2026"
    dias_afastamento = models.PositiveIntegerField(default=0)
    data_emissao = models.DateField(default=date.today)
    medico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Atestado {self.id}"

class ExameAnexado(models.Model):
    evolucao = models.ForeignKey(Evolucao, on_delete=models.CASCADE, related_name='exames_anexados')
    titulo = models.CharField(max_length=150)
    arquivo = models.FileField(upload_to='exames/%Y/%m/%d/')
    tipo = models.CharField(max_length=20, choices=[('pdf', 'PDF'), ('imagem', 'Imagem'), ('outro', 'Outro')], default='outro')
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    
