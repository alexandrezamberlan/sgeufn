#from django.conf.urls import url
from django.urls import path
from .views import RelatorioListView, RelatorioCreateView, RelatorioDetailView
from .views import RelatorioUpdateView, RelatorioDeleteView

urlpatterns = [
    path('list/', RelatorioListView.as_view(), name='relatorio_list'),
    path('cad/', RelatorioCreateView.as_view(), name='relatorio_create'),
    path('<slug:slug>/', RelatorioUpdateView.as_view(), name='relatorio_update'),
    path('<slug:slug>/delete/', RelatorioDeleteView.as_view(), name='relatorio_delete'),
    path('<slug:slug>/detalhes/', RelatorioDetailView.as_view(), name='relatorio_detail'),
]
