from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView

from aviso.models import Aviso

from utils.decorators import LoginRequiredMixin,  CoordenadorRequiredMixin

class HomeRedirectView(LoginRequiredMixin, CoordenadorRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('home')
    
class HomeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        if self.request.user.tipo == 'ADMINISTRADOR' or self.request.user.tipo == 'COORDENADOR' or self.request.user.tipo == 'MINISTRANTE':
            return reverse('home')
        elif self.request.user.tipo == 'PARTICIPANTE':
            return reverse('appmembro_home')   
        
        
class HomeView(LoginRequiredMixin, CoordenadorRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avisos'] = Aviso.ativos.filter(destinatario__in=[self.request.user.tipo, 'TODOS'])[0:2]
        return context


class AboutView(TemplateView):
	template_name = 'core/about.html'