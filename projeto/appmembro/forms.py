from django import forms

from evento.models import Evento
from inscricao.models import Inscricao
from usuario.models import Usuario


class MembroCreateForm(forms.ModelForm):
    nome = forms.CharField(label='Nome completo *', help_text='* Campos obrigatórios',required=True)
    
    instituicao = forms.CharField(label='Instituição a que pertence *', help_text='Registre a instituição, ou universidade, ou empresa',required=True)
    email = forms.EmailField(label='Email *', help_text='Use o email válido. Será usado para acessar sistema e recuperar senha!',required=True)
    celular = forms.CharField(label='Número celular com DDD *', help_text="Use DDD, por exemplo 55987619832",required=True)
    cpf = forms.CharField(label='CPF *',required=True)       
    
        
    class Meta:
        model = Usuario
        fields = ['nome','instituicao', 'email', 'celular', 'cpf']


class InscricaoForm(forms.ModelForm):
    evento = forms.ModelChoiceField(label='Evento', queryset=Evento.eventos_ativos_data_aberta.all())
    
    class Meta:
        model = Inscricao
        fields = []
        