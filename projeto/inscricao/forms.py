from django import forms
from django.db import models

from evento.models import Evento
from usuario.models import Usuario
from .models import Inscricao

class BuscaInscricaoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
class InscricaoForm(forms.ModelForm):
    # fields = ['evento', 'participante', 'is_active']
    evento = forms.ModelChoiceField(label='Evento ', queryset=Evento.eventos_ativos_data_aberta.all())
    participante = forms.ModelChoiceField(label='Participante', queryset=Usuario.usuarios_ativos.all())
   

    class Meta:
        model = Inscricao
        fields = ['evento', 'participante', 'is_active']

    def __init__(self, usuario_logado=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario_logado and usuario_logado.tipo == 'COORDENADOR':
            self.fields['evento'].queryset = Evento.eventos_ativos_data_aberta.filter(coordenador=usuario_logado)
        # self.fields['participante'].label_from_instance = self.label_from_instance_custom

    # def label_from_instance_custom(self, obj):
    #     texto = obj.apelido
    #     if obj.nome != obj.apelido:
    #         texto += f' | {obj.nome} '
    #     return texto

    
    