from django.db import models


class Sintoma(models.Model):
    """Lista de sintomas para consulta clínica assistida."""
    nome = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Condicao(models.Model):
    """Condição clínica / causa provável para agrupamento de sintomas."""
    nome = models.CharField(max_length=150, unique=True)
    descricao = models.TextField(blank=True)
    cid = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name_plural = 'Condições'

    def __str__(self):
        return self.nome


class SintomaCondicao(models.Model):
    """Peso da relação sintoma→condição. Ajustado automaticamente com uso do sistema."""
    sintoma = models.ForeignKey(Sintoma, on_delete=models.CASCADE, related_name='condicoes')
    condicao = models.ForeignKey(Condicao, on_delete=models.CASCADE, related_name='sintomas')
    peso = models.FloatField(default=1.0, help_text="Relevância deste sintoma para a condição (>= 0.05)")

    class Meta:
        unique_together = ('sintoma', 'condicao')

    def __str__(self):
        return f"{self.sintoma.nome} → {self.condicao.nome} ({self.peso:.2f})"


class CondicaoExameSugerida(models.Model):
    condicao = models.ForeignKey(Condicao, on_delete=models.CASCADE, related_name='exames_sugeridos')
    exame = models.ForeignKey('exames.Exame', on_delete=models.CASCADE)
    peso = models.FloatField(default=1.0)

    class Meta:
        unique_together = ('condicao', 'exame')
        verbose_name_plural = 'Exames sugeridos por condição'

    def __str__(self):
        return f"{self.condicao.nome} → {self.exame.nome}"


class CondicaoMedicamentoSugerido(models.Model):
    condicao = models.ForeignKey(Condicao, on_delete=models.CASCADE, related_name='medicamentos_sugeridos')
    medicamento = models.ForeignKey('receituario.Medicamento', on_delete=models.CASCADE)
    peso = models.FloatField(default=1.0)
    posologia_sugerida = models.CharField(max_length=200, blank=True,
                                          help_text="Posologia padrão sugerida ao médico")

    class Meta:
        unique_together = ('condicao', 'medicamento')
        verbose_name_plural = 'Medicamentos sugeridos por condição'

    def __str__(self):
        return f"{self.condicao.nome} → {self.medicamento.nome}"


class AnaliseClinica(models.Model):
    """Registro de uma análise clínica assistida, com resultado e feedback do médico."""
    paciente = models.ForeignKey('prontuario.Pacientes', on_delete=models.CASCADE)
    medico = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    sintomas = models.ManyToManyField(Sintoma, through='AnaliseSintoma')
    condicao_escolhida = models.ForeignKey(Condicao, on_delete=models.SET_NULL, null=True, blank=True)
    aceitou_sugestao = models.BooleanField(default=False, help_text="O médico aceitou a principal sugestão")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise {self.id} - {self.paciente.nome}"

    class Meta:
        ordering = ['-criado_em']


class AnaliseSintoma(models.Model):
    analise = models.ForeignKey(AnaliseClinica, on_delete=models.CASCADE)
    sintoma = models.ForeignKey(Sintoma, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=True, help_text="Médico confirmou este sintoma")

    class Meta:
        unique_together = ('analise', 'sintoma')
