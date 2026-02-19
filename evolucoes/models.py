from datetime import date
from django.db import models
from django.contrib.auth.models import User
from prontuario.models import Pacientes

class Evolucao(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to="fotos")
    evolucao = models.TextField()
    data_criacao = models.DateField(default=date.today)
    
    def __str__(self):
        return f"{self.titulo} - {self.paciente.nome}"
    