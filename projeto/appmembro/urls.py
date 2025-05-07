from __future__ import unicode_literals
from django.urls import path

from core.views import HomeRedirectView

from .views import (DadosMembroUpdateView,
                    EventoListView,  # InscricaoListView, InscricaoCreateView, InscricaoDeleteView,
                    HomeView, AboutView)

urlpatterns = [
   path('home', HomeView.as_view(), name='appmembro_home'), 
   # path('', HomeRedirectView.as_view(), name='home_redirect'),
   path('about', AboutView.as_view(), name='appmembro_about'),
   path('eventos/', EventoListView.as_view(), name='appmembro_evento_list'),

   path('meus-dados/', DadosMembroUpdateView.as_view(), name='appmembro_dados_update'),

   
   # path('minhas-submissoes/pendente/<slug:slug>/', SubmissaoPendenteUpdateView.as_view(), name='appmembro_submissao_pendente_update'),
   # path('minhas-submissoes/aprovado/<slug:slug>/', SubmissaoAprovadoUpdateView.as_view(), name='appmembro_submissao_aprovado_update'),
   

]
