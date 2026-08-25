from django.contrib import admin
from .models import Medicamento, Receita, ReceitaItem


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'principio_ativo', 'uso_count', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'principio_ativo')


class ReceitaItemInline(admin.TabularInline):
    model = ReceitaItem
    extra = 1


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'evolucao', 'medico', 'data_emissao', 'origem_sugestao')
    list_filter = ('data_emissao',)
    inlines = [ReceitaItemInline]
