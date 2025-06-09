from django import forms
from django.db import models

from inscricao.models import Inscricao
from .models import Frequencia

class BuscaFrequenciaForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    

class FrequenciaForm(forms.ModelForm):
    # fields = ['inscricao']
    inscricao = forms.ModelChoiceField(label='Inscrição ', queryset=Inscricao.objects.all())
   

    class Meta:
        model = Frequencia
        fields = ['inscricao']

    def __init__(self, usuario_logado=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if usuario_logado and usuario_logado.tipo == 'COORDENADOR':
            self.fields['inscricao'].queryset = Inscricao.objects.filter(evento__coordenador=usuario_logado)
        