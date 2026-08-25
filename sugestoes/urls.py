from django.urls import path
from . import views

app_name = 'sugestoes'

urlpatterns = [
    path('analise/<int:evolucao_id>/', views.analise_clinica, name='analise_clinica'),
    path('buscar-sintomas/', views.buscar_sintomas, name='buscar_sintomas'),
]
