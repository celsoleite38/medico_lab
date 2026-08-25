from django import forms
from .models import Atestado


class AtestadoForm(forms.ModelForm):
    class Meta:
        model = Atestado
        fields = ['modelo', 'cid', 'periodo', 'dias_afastamento', 'observacoes']
        widgets = {
            'modelo': forms.Select(attrs={'class': 'form-select'}),
            'cid': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex.: J06.9'
            }),
            'periodo': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Ex.: de 18/02 a 25/02/2026'
            }),
            'dias_afastamento': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Observações adicionais...',
            }),
        }

    def __init__(self, *args, modelo=None, **kwargs):
        super().__init__(*args, **kwargs)
        if modelo:
            self.instance.modelo = modelo
            self.fields.pop('modelo')
        else:
            self.fields['modelo'].queryset = self.fields['modelo'].queryset.filter(ativo=True)
