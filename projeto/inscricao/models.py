from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


from utils.gerador_hash import gerar_hash, gerar_chave_codigo_matricula


class Inscricao(models.Model):       
    participante = models.ForeignKey('usuario.Usuario', verbose_name='Inscrito no evento *', on_delete=models.PROTECT, related_name='participante')
    evento = models.ForeignKey('evento.Evento', verbose_name= 'Evento da inscrição *', on_delete=models.PROTECT, related_name='evento')
    data_hora_inscricao = models.DateTimeField(auto_now_add=True)
    codigo_matricula = models.CharField('Código matrícula gerado por hash *', max_length=20)
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, a inscrição pode ser usada no sistema')
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    

    class Meta:
        ordering            =   ['-is_active','evento','participante']
        verbose_name        =   'inscrição'
        verbose_name_plural =   'inscrições'

    def __str__(self):
        return '%s | %s - %s' % (self.participante, self.evento, self.codigo_matricula)
        
    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()
        
        self.codigo_matricula = gerar_chave_codigo_matricula(self.participante.email + self.evento.nome)
        
        #rotina para enviar por email a confirmação de inscrição com o código de matrícula gerado
        
        
        super(Inscricao, self).save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('inscricao_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('inscricao_delete', kwargs={'slug': self.slug})
