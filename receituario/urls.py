from django.urls import path
from . import views

app_name = 'receituario'

urlpatterns = [
    path('', views.lista_receitas, name='lista_receitas'),
    path('buscar/', views.buscar_medicamentos, name='buscar_medicamentos'),
    path('novo/<int:evolucao_id>/', views.nova_receita, name='nova_receita'),
    path('paciente/<int:paciente_id>/novo/', views.nova_receita, name='nova_receita_paciente'),
    path('pdf/<int:receita_id>/', views.receita_pdf, name='receita_pdf'),
]
