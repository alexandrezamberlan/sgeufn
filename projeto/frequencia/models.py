from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


from utils.gerador_hash import gerar_hash, gerar_chave_codigo_matricula


class Frequencia(models.Model):           
    inscricao = models.OneToOneField('inscricao.Inscricao', verbose_name='Inscrição do evento *', on_delete=models.PROTECT, related_name='inscricao')
    data_hora_frequencia = models.DateTimeField(auto_now_add=True)
    codigo_frequencia = models.CharField('Código de frequência', max_length=20, null=True, blank=True, help_text='Use o código de frequência informado pela organização do evento.')

    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    

    class Meta:
        ordering            =   ['inscricao__participante__nome']
        unique_together     =   ['inscricao','codigo_frequencia']
        verbose_name        =   'frequência'
        verbose_name_plural =   'frequências'

    def __str__(self):
        return '%s | %s' % (self.inscricao, self.data_hora_frequencia)
        
    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()        
        super(Frequencia, self).save(*args, **kwargs)    

    @property
    def get_delete_url(self):
        return reverse('frequencia_delete', kwargs={'slug': self.slug})
