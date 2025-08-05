from __future__ import unicode_literals

from django.contrib import messages

from django.db.models import Q

from django.shortcuts import redirect

from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView

from django.urls import reverse

from utils.decorators import LoginRequiredMixin, CoordenadorRequiredMixin, StaffRequiredMixin

from .models import Frequencia
from inscricao.models import Inscricao

from .forms import BuscaFrequenciaForm, FrequenciaForm, FrequenciaViaInscricaoForm


class FrequenciaListView(LoginRequiredMixin, CoordenadorRequiredMixin, ListView):
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
        if self.request.user.tipo == 'ADMINISTRADOR':
            qs = super().get_queryset().all()       
        
        if self.request.user.tipo == 'COORDENADOR' or self.request.user.tipo == 'MINISTRANTE':
            qs = super().get_queryset().all()
            qs = qs.filter(inscricao__evento__coordenador=self.request.user)
         
        
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
 

class FrequenciaCreateView(LoginRequiredMixin, CoordenadorRequiredMixin, CreateView):
    model = Frequencia
    # fields = ['inscricao']
    form_class = FrequenciaForm
    success_url = 'frequencia_list'
    
    def get_form(self, form_class=None):
        return FrequenciaForm(usuario_logado=self.request.user, data=self.request.POST or None)
    
    def get_success_url(self):
        messages.success(self.request, 'Frequência realizada com sucesso na plataforma!')
        return reverse(self.success_url)
    
    
class FrequenciaViaInscricaoCreateView(LoginRequiredMixin, CoordenadorRequiredMixin, CreateView):
    model = Frequencia
    template_name = 'frequencia/frequencia_via_inscricao_form.html'
    form_class = FrequenciaViaInscricaoForm
    success_url = 'inscricao_list'
    
    def get_initial(self):
        initials = super().get_initial()
        initials['inscricao'] = Inscricao.objects.get(slug=self.request.GET.get('inscricao_slug'))
        return initials

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inscricao'] = Inscricao.objects.get(slug=self.request.GET.get('inscricao_slug'))
        return context

    # def form_valid(self, form):
    #     try:
    #         formulario = form.save(commit=False)
    #         formulario.inscricao = Inscricao.objects.get(slug=self.request.GET.get('inscricao_slug'))
            
    #         if formulario.inscricao.evento.codigo_frequencia != formulario.codigo_frequencia:
    #             messages.error(self.request, 'Código de frequência inválido. Verifique o código informado!')
    #             return super().form_invalid(form)
            
    #         formulario.save()

    #         return super().form_valid(form)

    #     except Exception as e:
    #         messages.error(self.request, 'Erro ao registrar frequência. Verifique se você já não realizaou a frequência neste evento!')
    #         return super().form_invalid(form)
    
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