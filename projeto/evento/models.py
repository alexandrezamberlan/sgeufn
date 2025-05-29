from __future__ import unicode_literals

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from utils.gerador_hash import gerar_hash

from inscricao.models import Inscricao

class EventoAtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    
class EventoAtivoComDataAbertaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, data_inscricao__gte=timezone.now().date())


class Evento(models.Model):       
    nome = models.CharField('Nome do evento *', unique=True, db_index=True, max_length=150, help_text='* Campo obrigatório')
    descricao = models.TextField('Descrição do evento', null=True, blank=True, max_length=500 ,help_text='Coque aqui uma descrição do evento para ajudar os autores a submeterem seus trabalhos')
    tipo = models.ForeignKey('tipo_evento.TipoEvento', verbose_name= 'Tipo do evento *', on_delete=models.PROTECT, related_name='tipo_evento')
    site = models.URLField('Site do evento', max_length=100, help_text='Informe o site oficial do evento', null=True, blank=True)   
    instituicao = models.ForeignKey('instituicao.Instituicao', verbose_name= 'Instituição responsável pelo evento *', on_delete=models.PROTECT, related_name='instituicao')
    data_inicio = models.DateField('Data do evento *', max_length=10, help_text='Use dd/mm/aaaa', null=True, blank=False)
    
    coordenador = models.ForeignKey('usuario.Usuario', verbose_name= 'Coordenador responsável *', on_delete=models.PROTECT, related_name='coordenador')
    email = models.EmailField('Email oficial da organização', max_length=100,help_text='Campo opcional, caso o evento seja de submissão de trabalhos.', null=True, blank=True)
    
    data_inscricao = models.DateField('Data limite de inscrição ao evento *', max_length=10, help_text='Use dd/mm/aaaa', null=True, blank=False)
    carga_horaria = models.DecimalField('Carga horária do evento ', max_digits=4, decimal_places=0, validators=[MinValueValidator(1), MaxValueValidator(12)], null=True, blank=False, default = 1)    
    local = models.CharField('Local do evento', max_length=300, help_text='Informe detalhes do local, como sala, prédio, conjunto, etc.', null=True, blank=True)
    lotacao = models.DecimalField('Lotação máxima do local do evento ', max_digits=4, decimal_places=0, validators=[MinValueValidator(1), MaxValueValidator(9999)], null=True, blank=True)    

    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o evento está liberado para chamada de artigos')    
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    eventos_ativos = EventoAtivoManager()
    eventos_ativos_data_aberta = EventoAtivoComDataAbertaManager()

    class Meta:
        ordering            =   ['-is_active','-data_inscricao','nome']
        verbose_name        =   'evento'
        verbose_name_plural =   'eventos'

    def __str__(self):
        return '%s | %s | %s' % (self.nome, self.data_inscricao.strftime("%d/%m/%Y"), self.instituicao.nome)

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
        self.nome = self.nome.upper()             
        super(Evento, self).save(*args, **kwargs)
        
    @property
    def get_data_atual(self):
        return timezone.now().date()

    @property
    def get_absolute_url(self):
        return reverse('evento_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('evento_delete', kwargs={'slug': self.slug})
    
    @property
    def quantidade_inscritos(self):
        return Inscricao.objects.filter(evento=self, is_active=True).count()
    
    @property
    def quantidade_vagas(self):
        if self.lotacao:
            return self.lotacao - self.quantidade_inscritos
        return 0
    
    @property
    def pode_inscrever_se(self):
        return self.data_inscricao >= self.get_data_atual and self.quantidade_vagas > 0

    @property
    def get_inscricao_create_url(self):
        return '%s?evento_slug=%s' % (reverse('appmembro_inscricao_create'), self.slug)