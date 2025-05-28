from __future__ import unicode_literals

import os

from django.contrib import messages
from django.db.models import ProtectedError

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, StaffRequiredMixin

from .models import Inscricao

from .forms import BuscaInscricaoForm


class InscricaoListView(LoginRequiredMixin, ListView):
    model = Inscricao

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            #quando ja tem dados filtrando
            context['form'] = BuscaInscricaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            context['form'] = BuscaInscricaoForm()
        return context

    def get_queryset(self):                
        qs = super().get_queryset().all()        
        
        if self.request.GET:
            #quando ja tem dados filtrando
            form = BuscaInscricaoForm(data=self.request.GET)
        else:
            #quando acessa sem dados filtrando
            form = BuscaInscricaoForm()

        if form.is_valid():            
            pesquisa = form.cleaned_data.get('pesquisa')            
                        
            if pesquisa:
                qs = qs.filter(Q(participante__nome__icontains=pesquisa) | Q(evento__nome__icontains=pesquisa) | Q(evento__descricao__icontains=pesquisa))            
            
        return qs
 

class InscricaoCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Inscricao
    fields = ['evento', 'participante', 'is_active']
    success_url = 'inscricao_list'
    
    def get_success_url(self):
        messages.success(self.request, 'Inscrição realizada com sucesso na plataforma!')
        return reverse(self.success_url)
    
    def form_valid(self, form):
        formulario = form.save(commit=False)
        
        if formulario.evento.quantidade_vagas <= 0:
            messages.error(self.request,"Não há mais vagas para este evento. Inscrição NÃO realizada. Aguarde liberar uma vaga!!!")  
            return super().form_invalid(form)
        
        formulario.save()

        return super().form_valid(form)   


# class InscricaoUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
#     model = Inscricao
#     fields = ['participante', 'evento', 'is_active']
#     success_url = 'inscricao_list'
    
#     def get_success_url(self):
#         messages.success(self.request, 'Instituição atualizada com sucesso na plataforma!')
#         return reverse(self.success_url) 


class InscricaoDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Inscricao
    success_url = 'inscricao_list'
    template_name = 'inscricao/inscricao_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Inscrição removida com sucesso na plataforma!')
        return reverse(self.success_url) 

    def post(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        try:           
            self.object = self.get_object()
            self.object.delete()
            success_url = self.get_success_url()
            self.object.delete()
        except Exception as e:
            messages.error(request, 'Há dependências ligadas à essa Inscrição, permissão negada!')
        return redirect(self.success_url)
