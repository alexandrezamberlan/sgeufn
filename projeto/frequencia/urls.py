from django.urls import path

from .views import FrequenciaListView, FrequenciaCreateView
from .views import FrequenciaDeleteView


urlpatterns = [
	path('list/', FrequenciaListView.as_view(), name='frequencia_list'),
	path('cad/', FrequenciaCreateView.as_view(), name='frequencia_create'),	
	path('<slug:slug>/delete/', FrequenciaDeleteView.as_view(), name='frequencia_delete'), 
]
 