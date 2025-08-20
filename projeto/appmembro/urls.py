from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosMembroUpdateView, FrequenciaCreateView, InscricaoPdfView, InscricaoDetailView,
                    EventoListView,  InscricaoListView, InscricaoCreateView, InscricaoDeleteView,
                    HomeView, AboutView, AutenticaListView, AtestadoManualListView, EventoMinistradoListView,
                    MinistrantePdfView)

urlpatterns = [
   path('home', HomeView.as_view(), name='appmembro_home'), 
   path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appmembro_about'),

   path('meus-dados/', DadosMembroUpdateView.as_view(), name='appmembro_dados_update'),
   
   path('minhas-frequencias/cad/', FrequenciaCreateView.as_view(), name='appmembro_frequencia_create'),
   path('minhas-inscricoes', InscricaoListView.as_view(), name='appmembro_inscricao_list'),
   path('minhas-participacoes', EventoMinistradoListView.as_view(), name='appmembro_eventoministrado_list'),
   path('minhas-inscricoes/cad/', InscricaoCreateView.as_view(), name='appmembro_inscricao_create'),
   
   path('<slug:slug>/detalhes/', InscricaoDetailView.as_view(), name='appmembro_inscricao_detail'),
   path('<slug:slug>/delete/', InscricaoDeleteView.as_view(), name='appmembro_inscricao_delete'), 
   
   path('inscricao/<slug:slug>/pdf/', InscricaoPdfView.as_view(), name='appmembro_inscricao_pdf'),
   path('ministrante/<slug:slug>/pdf/', MinistrantePdfView.as_view(), name='appmembro_ministrante_pdf'),
   
   path('eventos/', EventoListView.as_view(), name='appmembro_evento_list'),
   
   path('autenticacao', AutenticaListView.as_view(), name='appmembro_autentica'),
   
   path('meus-atestados/list/', AtestadoManualListView.as_view(), name='appmembro_atestado_manual_list'),

]
