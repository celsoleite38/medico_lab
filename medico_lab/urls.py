from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from medico_lab import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

def test_view(request):
    return HttpResponse("Prontario URLs funcionando!")

urlpatterns = [
    path('test/', test_view, name="test"),  # URL de teste
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls')),
    path('', RedirectView.as_view(url='/auth/logar/', permanent=False)),
    path('evolucoes/', include('evolucoes.urls', namespace='evolucoes')),
    path('prontuario/', include('prontuario.urls', namespace='prontuario')),
    path('agenda/', include('agenda.urls',namespace='agenda')),
    path('notificacoes/', include('notificacoes.urls')),
    path('exames/', include('exames.urls', namespace='exames')),
    path('receituario/', include('receituario.urls', namespace='receituario')),
    path('atestados/', include('atestados.urls', namespace='atestados')),
    path('sugestoes/', include('sugestoes.urls', namespace='sugestoes')),
    # Páginas de vendas/pagamentos (rotas absolutas como /teste-gratis/ e /pagamento/)
    # Montado após o redirect de '/' para preservar o comportamento da home.
    path('', include('paginas_vendas.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)