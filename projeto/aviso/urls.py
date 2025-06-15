from django.urls import path

from .views import AvisoListView, AvisoCreateView
from .views import AvisoUpdateView, AvisoDeleteView, AvisoEnviaEmail, AvisoListIFrameView

urlpatterns = [
	path('list/', AvisoListView.as_view(), name='aviso_list'),
	path('cad/', AvisoCreateView.as_view(), name='aviso_create'),
	path('<slug:slug>/', AvisoUpdateView.as_view(), name='aviso_update'),
	path('<slug:slug>/delete/', AvisoDeleteView.as_view(), name='aviso_delete'), 
 	path('<slug:slug>/envia-email/', AvisoEnviaEmail.as_view(), name='aviso_envia_email'),
	path('list/iframe', AvisoListIFrameView.as_view(), name='aviso_list_iframe'),
]
 