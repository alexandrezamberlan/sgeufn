from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.urls import reverse

from avaliacao.models import Avaliacao
from submissao.models import Submissao
from utils.gerador_hash import gerar_hash


class Relatorio(models.Model):
    titulo = models.CharField('Titulo *', max_length=200, unique=True)
    descricao = models.TextField('Detalhamento do relatório *')
    script_sql = models.TextField('Script SQL', null=True, blank=True)
    resposta = models.TextField('Respostas do relatório', null=True, blank=True)
    data = models.DateField('Data de geração do relatório *', default=datetime.now)
    # responsavel import de Usuario
    slug = models.SlugField('Hash',max_length= 200, null=True, blank=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['-data', 'titulo']
        verbose_name = 'relatório'
        verbose_name_plural = 'relatórios'

    def __str__(self):
        return '%s | %s' % (self.titulo, self.data.strftime('%d/%m/%Y'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = gerar_hash()
        self.titulo = self.titulo.upper()
        super(Relatorio, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('relatorio_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('relatorio_delete', kwargs={'slug': self.slug})

    @property
    def get_visualiza_url(self):
        return reverse('relatorio_detail', kwargs={'slug': self.slug})