from django.contrib import admin
from .models import (
    Sintoma, Condicao, SintomaCondicao,
    CondicaoExameSugerida, CondicaoMedicamentoSugerido,
    AnaliseClinica, AnaliseSintoma,
)


@admin.register(Sintoma)
class SintomaAdmin(admin.ModelAdmin):
    search_fields = ('nome',)


@admin.register(Condicao)
class CondicaoAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('nome', 'cid')


@admin.register(SintomaCondicao)
class SintomaCondicaoAdmin(admin.ModelAdmin):
    list_display = ('sintoma', 'condicao', 'peso')
    list_filter = ('condicao',)


@admin.register(CondicaoExameSugerida)
class CondicaoExameSugeridaAdmin(admin.ModelAdmin):
    list_display = ('condicao', 'exame', 'peso')
    list_filter = ('condicao',)


@admin.register(CondicaoMedicamentoSugerido)
class CondicaoMedicamentoSugeridoAdmin(admin.ModelAdmin):
    list_display = ('condicao', 'medicamento', 'peso', 'posologia_sugerida')
    list_filter = ('condicao',)


class AnaliseSintomaInline(admin.TabularInline):
    model = AnaliseSintoma
    extra = 0


@admin.register(AnaliseClinica)
class AnaliseClinicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'condicao_escolhida', 'aceitou_sugestao', 'criado_em')
    list_filter = ('aceitou_sugestao',)
    inlines = [AnaliseSintomaInline]
