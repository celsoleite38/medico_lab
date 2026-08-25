from django.db import models
from django.utils import timezone


class ModeloAtestado(models.Model):
    """Templates disponíveis para emissão de atestado."""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    # Template com placeholders: {{paciente}}, {{data_hoje}}, {{medico}}, {{periodo}}, {{dias}}, {{cid}}, {{local}}, {{clinica}}
    texto_template = models.TextField(
        help_text="Use {{variavel}} para campos dinâmicos. "
                  "Variáveis: paciente, data_hoje, medico, periodo, dias, cid, local, clinica"
    )
    requer_dias = models.BooleanField(default=False)
    requer_periodo = models.BooleanField(default=False)
    requer_cid = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Atestado(models.Model):
    evolucao = models.ForeignKey('evolucoes.Evolucao', on_delete=models.CASCADE, related_name='atestados')
    medico = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    modelo = models.ForeignKey(ModeloAtestado, on_delete=models.PROTECT)
    cid = models.CharField(max_length=10, blank=True, help_text="Código CID-10, se aplicável")
    periodo = models.CharField(max_length=100, blank=True, help_text="Ex.: 'de 18/02 a 25/02/2026'")
    dias_afastamento = models.PositiveIntegerField(default=0)
    observacoes = models.TextField(blank=True)
    texto_final = models.TextField(blank=True)
    data_emissao = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-data_emissao']

    def __str__(self):
        return f"Atestado {self.id} - {self.evolucao.paciente.nome}"

    def renderizar(self):
        from autenticacao.models import PerfilProfissional

        paciente = self.evolucao.paciente
        perfil = PerfilProfissional.objects.filter(usuario=self.medico).first()
        dados = {
            'paciente': paciente.nome,
            'data_hoje': self.data_emissao.strftime('%d/%m/%Y'),
            'medico': perfil.nome_completo if perfil else self.medico.get_full_name(),
            'periodo': self.periodo,
            'dias': str(self.dias_afastamento),
            'cid': self.cid,
            'local': perfil.endereco if perfil else '',
            'clinica': perfil.nomeclinica if perfil else '',
        }
        texto = self.modelo.texto_template
        for chave, valor in dados.items():
            texto = texto.replace(f'{{{{{chave}}}}}', valor)
        return texto
