
# documentos/urls.py
from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    path('receituario/adicionar/<int:evolucao_id>/', views.adicionar_receituario, name='adicionar_receituario'),
    path('receituario/pdf/<int:receituario_id>/', views.gerar_pdf_receituario, name='pdf_receituario'),
    
    path('pedido_exame/adicionar/<int:evolucao_id>/', views.adicionar_pedido_exame, name='adicionar_pedido_exame'),
    #path('pedido_exame/pdf/<int:pedido_id>/', views.gerar_pdf_pedido, name='pdf_pedido_exame'),
    path('exame_anexado/adicionar/<int:evolucao_id>/', views.adicionar_exame_anexado, name='adicionar_exame_anexado'),
    
    path('atestado/adicionar/<int:evolucao_id>/', views.adicionar_atestado, name='adicionar_atestado'),
    
]