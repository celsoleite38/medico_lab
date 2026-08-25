from django.contrib import admin
from .models import ModeloAtestado, Atestado


@admin.register(ModeloAtestado)
class ModeloAtestadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'requer_dias', 'requer_periodo', 'requer_cid', 'ativo')
    list_filter = ('ativo',)


@admin.register(Atestado)
class AtestadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'evolucao', 'modelo', 'medico', 'data_emissao', 'dias_afastamento')
    list_filter = ('modelo', 'data_emissao')
