from django import forms
from .models import Pacientes

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['nome', 'sexo', 'cpf', 'estadocivil', 'datanascimento', 'naturalidade', 'profissao', 'email', 'telefone', 'endereco']
        
        



