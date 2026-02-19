from django.contrib import admin
from django.contrib.auth.models import User 
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

from evolucoes.models import Evolucao
import prontuario
from .models import Pacientes, DadosPaciente

class PacientesResource(resources.ModelResource):

    medico = fields.Field(
        column_name='medico',
        attribute='medico',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Pacientes
        import_id_fields = ('nome',)
        fields = ('nome', 'cpf', 'sexo', 'estadocivil', 'datanascimento', 
                  'naturalidade', 'profissao', 'email', 'telefone', 'endereco', 'medico')

@admin.register(Pacientes)
class PacientesAdmin(ImportExportModelAdmin):
    resource_class = PacientesResource
    list_display = ('nome', 'medico', 'datanascimento') 
    list_filter = ('medico',)


class DadosPacienteResource(resources.ModelResource):
    paciente = fields.Field(
        column_name='paciente',
        attribute='paciente',
        widget=ForeignKeyWidget(Pacientes, 'nome')
    )

    class Meta:
        model = DadosPaciente

        fields = (
            'id', 'paciente', 'peso', 'qp', 'hma', 'hpp', 
            'antecedentepf', 'exame_fisico', 'exames_complementares', 
            'diagnostico', 'plano_terapeutico', 'data_dadospaciente'
        )
        import_id_fields = ('paciente',)

@admin.register(DadosPaciente)
class DadosPacienteAdmin(ImportExportModelAdmin):
    resource_class = DadosPacienteResource
    list_display = ('paciente', 'data_dadospaciente')
    search_fields = ('paciente__nome',)