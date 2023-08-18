from django.urls import path
from .views import MarcacoesView, MarcacoesCreate, RelatorioFormView, RelatorioDownload

urlpatterns = [
    path('', MarcacoesView.as_view(), name='marcacoes'),
    path('inserir-marcacao', MarcacoesCreate.as_view(), name='inserir-marcacao'),
    path('relatorio-form', RelatorioFormView.as_view(), name='relatorio-form'),
    path('relatorio-download-<int:user_id>-<int:mes_ref>', RelatorioDownload.as_view(), name='relatorio-download'),    
]