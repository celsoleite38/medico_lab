# evolucoes/urls.py
from django.urls import path
from . import views

app_name = 'evolucoes'

urlpatterns = [
    
    #path('paciente/<int:paciente_id>/evolucoes/', views.plano_evolucao, name='plano_evolucao'),
    path('evolucao/<int:evolucao_id>/', views.detalhe_evolucao, name='detalhe_evolucao'),
    
]