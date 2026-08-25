from django.contrib import admin
from .models import Exame, ValorReferencia, PedidoExame, ItemPedidoExame, ResultadoExame, MedicaoResultado


class ValorReferenciaInline(admin.TabularInline):
    model = ValorReferencia
    extra = 0


@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'uso_count', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome', 'codigo_tuss')
    inlines = [ValorReferenciaInline]


@admin.register(ValorReferencia)
class ValorReferenciaAdmin(admin.ModelAdmin):
    list_display = ('analito', 'exame', 'unidade', 'valor_min', 'valor_max', 'genero')
    list_filter = ('exame', 'genero')


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedidoExame
    extra = 1


@admin.register(PedidoExame)
class PedidoExameAdmin(admin.ModelAdmin):
    list_display = ('id', 'evolucao', 'medico', 'data_pedido')
    list_filter = ('data_pedido',)
    inlines = [ItemPedidoInline]


@admin.register(MedicaoResultado)
class MedicaoResultadoAdmin(admin.ModelAdmin):
    list_display = ('analito', 'valor', 'unidade', 'status', 'resultado')
    list_filter = ('status',)
