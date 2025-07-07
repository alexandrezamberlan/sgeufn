from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import AtestadoManual

from .forms import BuscaAtestadoManualForm


class AtestadoManualListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = AtestadoManual

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaAtestadoManualForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaAtestadoManualForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        

        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaAtestadoManualForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaAtestadoManualForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(nome__icontains=pesquisa) | Q(atividade__icontains=pesquisa) | Q(responsavel__icontains=pesquisa))
            
        return qs
 

class AtestadoManualCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = AtestadoManual
    fields = ['nome', 'tipo', 'ministrantes', 'descricao', 'carga_horaria', 'local', 'lotacao', 'site', 'grupo', 'instituicao', 'coordenador', 'email', 'data_inicio', 'hora_inicio', 'data_inscricao', 'frequencia_liberada', 'codigo_frequencia', 'is_active']
    success_url = 'atestado_manual_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Atestado cadastrado com sucesso na plataforma!')
        return reverse(self.success_url)


class AtestadoManualUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = AtestadoManual
    fields = ['nome', 'tipo', 'ministrantes', 'descricao', 'carga_horaria', 'local', 'lotacao', 'site', 'grupo', 'instituicao', 'coordenador', 'email', 'data_inicio', 'hora_inicio', 'data_inscricao', 'frequencia_liberada', 'codigo_frequencia', 'is_active']
    success_url = 'atestado_manual_list'    

    def get_success_url(self):
        messages.success(self.request, 'Atestado atualizado com sucesso na plataforma!')
        return reverse(self.success_url) 


class AtestadoManualDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = AtestadoManual
    success_url = 'atestado_manual_list'

    def get_success_url(self):
        messages.success(self.request, 'Atestado removido com sucesso da plataforma!')
        return reverse(self.success_url) 

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        try:
            self.object = self.get_object()
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à esse Atestado, permissão negada!')
        return redirect(self.success_url)