from django import forms
from .models import Receita, ReceitaItem


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['observacoes_gerais']
        widgets = {
            'observacoes_gerais': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Observações gerais do receituário...',
            }),
        }


class ReceitaItemForm(forms.ModelForm):
    class Meta:
        model = ReceitaItem
        fields = ['medicamento', 'dosagem', 'quantidade', 'posologia', 'observacoes_item']
        widgets = {
            'medicamento': forms.Select(attrs={'class': 'form-select'}),
            'dosagem': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex.: 20mg'
            }),
            'quantidade': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex.: 30 comprimidos'
            }),
            'posologia': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2,
                'placeholder': 'Ex.: 1 comprimido de 12/12h por 7 dias'
            }),
            'observacoes_item': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Observações (opcional)'
            }),
        }


ReceitaItemFormSet = forms.inlineformset_factory(
    Receita, ReceitaItem, form=ReceitaItemForm,
    extra=1, can_delete=True,
)
