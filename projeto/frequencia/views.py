from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import Frequencia

from .forms import BuscaFrequenciaForm


class FrequenciaListView(LoginRequiredMixin, ListView):
    model = Frequencia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaFrequenciaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaFrequenciaForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaFrequenciaForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaFrequenciaForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(inscricao__participante__nome__icontains=pesquisa) | Q(inscricao__evento__nome__icontains=pesquisa) | Q(inscricao__evento__descricao__icontains=pesquisa))            
            
        return qs
 

class FrequenciaCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Frequencia
    fields = ['inscricao']
    success_url = 'frequencia_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Frequência realizada com sucesso na plataforma!')
        return reverse(self.success_url)


class FrequenciaDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Frequencia
    success_url = 'frequencia_list'

    def get_success_url(self):
        messages.success(self.request, 'Frequência removida com sucesso na plataforma!')
        return reverse(self.success_url) 

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Frequência, permissão negada!')
        return redirect(self.success_url)