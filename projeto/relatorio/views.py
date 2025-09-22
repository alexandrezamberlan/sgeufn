from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from utils.decorators import LoginRequiredMixin

from .models import Relatorio
from .conecta_llm import Conecta


class RelatorioListView(LoginRequiredMixin, ListView):
    model = Relatorio


class RelatorioCreateView(LoginRequiredMixin, CreateView):
    model = Relatorio
    fields = ['titulo','descricao']
    success_url = 'relatorio_list'

    def get_success_url(self):
        messages.success(self.request, 'Relatorio gerado com sucesso na plataforma!')
        return reverse(self.success_url)
    
    def form_valid(self, form):
        relatorio = form.save()

        # aplicar conexao pandas - trabalho Pedro
        #relatorio.resposta = Conecta.gera_dataframe()
        
        # aplicar conexao gemini api - llm
        relatorio.script_sql = Conecta.gera_sql(relatorio.descricao)
        
        # aplicar script sql
        relatorio.resposta = Conecta.executa_sql(relatorio.script_sql)
        
        relatorio.save()
        return super(RelatorioCreateView, self).form_valid(form)


class RelatorioUpdateView(LoginRequiredMixin, UpdateView):
    model = Relatorio
    fields = ['titulo','descricao']
    success_url = 'relatorio_list'

    def get_success_url(self):
        messages.success(self.request, 'Relatorio atualizado com sucesso na plataforma!')
        return reverse(self.success_url)
    
    def form_valid(self, form):
        relatorio = form.save()
        
        # aplicar conexao pandas - trabalho Pedro
        #relatorio.resposta = Conecta.gera_dataframe()
        
        # aplicar conexao rpc - llm - trabalho Luiz
        relatorio.script_sql = Conecta.gera_sql(relatorio.descricao)
        # aplicar script sql
        relatorio.resposta = Conecta.executa_sql(relatorio.script_sql)
        
        relatorio.save()
        return super(RelatorioUpdateView, self).form_valid(form)


class RelatorioDeleteView(LoginRequiredMixin, DeleteView):
    model = Relatorio
    success_url = 'relatorio_list'

    def get_success_url(self):
        messages.success(self.request, 'Relatorio removido com sucesso na plataforma!')
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
            messages.error(request, 'Há dependências ligadas à esse Relatório, permissão negada!')
        return redirect(self.success_url)
    
    
class RelatorioDetailView(LoginRequiredMixin, DetailView):
    model = Relatorio
    template_name = 'relatorio/relatorio_detail.html'
    
