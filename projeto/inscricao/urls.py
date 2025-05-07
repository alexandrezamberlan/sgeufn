from django.urls import path

from .views import InscricaoListView, InscricaoCreateView
from .views import InscricaoDeleteView


urlpatterns = [
	path('list/', InscricaoListView.as_view(), name='inscricao_list'),
	path('cad/', InscricaoCreateView.as_view(), name='inscricao_create'),
	# path('<slug:slug>/', InscricaoUpdateView.as_view(), name='inscricao_update'),
	path('<slug:slug>/delete/', InscricaoDeleteView.as_view(), name='inscricao_delete'), 
]
 