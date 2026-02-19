from django.contrib import admin
from .models import Medicamento, Receituario, ReceituarioItem, Atestado, PedidoExame, ExameAnexado

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'principio_ativo', 'created_at')
    search_fields = ('nome', 'principio_ativo')
    list_filter = ('created_at',)
    ordering = ('nome',)

# Registre os outros modelos também (opcional, mas útil)
admin.site.register(Receituario)
admin.site.register(ReceituarioItem)
admin.site.register(Atestado)
admin.site.register(PedidoExame)
admin.site.register(ExameAnexado)