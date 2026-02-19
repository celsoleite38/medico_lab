# evolucoes/admin.py
from django.contrib import admin
from .models import Evolucao

@admin.register(Evolucao)
class EvolucaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'paciente', 'data_criacao')
    list_filter = ('data_criacao',)
    search_fields = ('titulo', 'evolucao', 'paciente__nome')