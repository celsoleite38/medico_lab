from django.urls import path
from . import views

app_name = 'exames'

urlpatterns = [
    path('', views.lista_pedidos, name='lista_pedidos'),
    path('resultados/', views.lista_resultados, name='lista_resultados'),
    path('buscar/', views.buscar_exames, name='buscar_exames'),
    path('novo/<int:evolucao_id>/', views.novo_pedido_exame, name='novo_pedido_exame'),
    path('paciente/<int:paciente_id>/novo/', views.novo_pedido_exame, name='novo_pedido_paciente'),
    path('pdf/<int:pedido_id>/', views.pedido_exame_pdf, name='pedido_exame_pdf'),
    path('upload/<int:paciente_id>/', views.upload_resultado, name='upload_resultado'),
    path('resultado/<int:resultado_id>/', views.ver_resultado, name='ver_resultado'),
]
