from django import forms
from .models import PedidoExame, ItemPedidoExame, ResultadoExame


class NovoPedidoExameForm(forms.ModelForm):
    class Meta:
        model = PedidoExame
        fields = ['justificativa_clinica']
        widgets = {
            'justificativa_clinica': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Justificativa clínica para os exames solicitados...',
            }),
        }


class ItemPedidoForm(forms.Form):
    """Form para adicionar um item a um pedido existente."""
    exame_id = forms.IntegerField(widget=forms.HiddenInput)
    instrucoes = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-control-sm',
        'placeholder': 'Instruções especiais (opcional)',
    }))


class UploadResultadoForm(forms.ModelForm):
    class Meta:
        model = ResultadoExame
        fields = ['titulo', 'arquivo', 'tipo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex.: Hemograma completo - Lab XYZ'
            }),
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
