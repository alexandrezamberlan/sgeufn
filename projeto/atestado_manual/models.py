from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from utils.gerador_hash import gerar_hash, gerar_chave_codigo_matricula

class AtestadoManual(models.Model):
    TIPOS_USUARIOS = (
        ('PARTICIPANTE', 'Participante'),
        ('MINISTRANTE', 'Ministrante'),
    )

    papel = models.CharField('Papel na atividade *', max_length=20, choices=TIPOS_USUARIOS, default='PARTICIPANTE', help_text='* Campo obrigatório. Se não tiver certeza, escolha Participante.')

    pessoa = models.ForeignKey('usuario.Usuario', verbose_name= 'Nome *', on_delete=models.PROTECT, related_name='pessoa', null=True, blank=False)
    atividade = models.TextField('Descrição da atividade', null=True, blank=True, max_length=500 ,help_text='Coloque aqui uma descrição do atestado_manual para ajudar os autores a submeterem seus trabalhos')
    
    instituicao = models.CharField('Departamento ou Setor ou Grupo responsável pela atividade *', null=True, blank=False, max_length=150, help_text='* Campo obrigatório')
    
    data_inicio = models.DateField('Data do início *', max_length=10, help_text='Use dd/mm/aaaa', null=True, blank=False)
    data_fim = models.DateField('Data do fim *', max_length=10, help_text='Use dd/mm/aaaa', null=True, blank=False)
    
    responsavel = models.CharField('Coordenador responsável *', max_length=150, help_text='* Campo obrigatório')

    carga_horaria = models.DecimalField('Carga horária da atividade ', max_digits=4, decimal_places=0, validators=[MinValueValidator(1), MaxValueValidator(180)], null=True, blank=False, default = 1, help_text='* Campo obrigatório. Use apenas números inteiros, sem ponto ou vírgula. Carga máxima de 180 dez horas.')
    
    codigo_matricula = models.CharField('Código matrícula gerado por hash *', max_length=20)
    
    is_active = models.BooleanField('Ativo', default=True, help_text='Se ativo, o evento está liberado para chamada de artigos')    
    slug = models.SlugField('Hash',max_length= 200,null=True,blank=True)

    objects = models.Manager()
    

    class Meta:
        unique_together     =   ['pessoa', 'codigo_matricula']
        ordering            =   ['-is_active','pessoa', '-data_inicio']
        verbose_name        =   'atestado'
        verbose_name_plural =   'atestados'

    def __str__(self):
        return '%s | %s ' % (self.pessoa.nome, self.atividade)

    def save(self, *args, **kwargs):        
        if not self.slug:
            self.slug = gerar_hash()   
        self.instituicao = self.instituicao.upper()         
        self.responsavel = self.responsavel.upper()     
        self.codigo_matricula = gerar_chave_codigo_matricula(self.pessoa.nome + self.atividade)
        super(AtestadoManual, self).save(*args, **kwargs)
        
    @property
    def get_data_atual(self):
        return timezone.now().date()

    @property
    def get_absolute_url(self):
        return reverse('atestado_manual_update', kwargs={'slug': self.slug})

    @property
    def get_delete_url(self):
        return reverse('atestado_manual_delete', kwargs={'slug': self.slug})
    