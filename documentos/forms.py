from django import forms
from .models import Atestado, ExameAnexado, PedidoExame, Receituario, ReceituarioItem
from django.forms import inlineformset_factory

class ReceituarioForm(forms.ModelForm):
    class Meta:
        model = Receituario
        fields = ['observacoes_gerais']
        widgets = {
            'observacoes_gerais': forms.Textarea(attrs={'rows': 3}),
        }

ReceituarioItemFormSet = inlineformset_factory(
    Receituario,
    ReceituarioItem,
    fields=('medicamento', 'dosagem', 'quantidade', 'posologia', 'observacoes_item'),
    extra=1,
    can_delete=True,
    widgets={
        'medicamento': forms.Select(attrs={'class': 'form-control select2'}),
        'dosagem': forms.TextInput(attrs={'class': 'form-control'}),
        'quantidade': forms.TextInput(attrs={'class': 'form-control'}),
        'posologia': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        'observacoes_item': forms.TextInput(attrs={'class': 'form-control'}),
    }
)
class PedidoExameForm(forms.ModelForm):
    class Meta:
        model = PedidoExame
        fields = ['exames_solicitados', 'justificativa_clinica']
        widgets = {
            'exames_solicitados': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'justificativa_clinica': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class AtestadoForm(forms.ModelForm):
    class Meta:
        model = Atestado
        fields = ['cid', 'descricao', 'periodo', 'dias_afastamento']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
            'periodo': forms.TextInput(attrs={'placeholder': 'ex.: de 18/02 a 25/02'}),
        }

class ExameAnexadoForm(forms.ModelForm):
    class Meta:
        model = ExameAnexado
        fields = ['titulo', 'arquivo']