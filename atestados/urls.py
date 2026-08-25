from django.urls import path
from . import views

app_name = 'atestados'

urlpatterns = [
    path('', views.lista_atestados, name='lista_atestados'),
    path('modelos/', views.modelos_atestado, name='modelos_atestado'),
    path('modelos/<int:paciente_id>/', views.modelos_atestado, name='modelos_atestado_paciente'),
    path('novo/<int:evolucao_id>/<int:modelo_id>/', views.novo_atestado, name='novo_atestado'),
    path('paciente/<int:paciente_id>/novo/<int:modelo_id>/', views.novo_atestado, name='novo_atestado_paciente'),
    path('pdf/<int:atestado_id>/', views.atestado_pdf, name='atestado_pdf'),
]
