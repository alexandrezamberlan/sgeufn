from django import forms
from django.db import models

from usuario.models import Usuario
from .models import Evento


class EventoForm(forms.ModelForm):
    coordenador = forms.ModelChoiceField(label='Coordenador responsável *', queryset=Usuario.coordenadores.all())
    
    class Meta:
        model = Evento
        fields = ['nome', 'tipo', 'descricao', 'carga_horaria', 'local', 'lotacao', 'site', 'grupo', 'instituicao', 'coordenador', 'email', 'data_inicio', 'hora_inicio', 'data_inscricao', 'frequencia_liberada', 'codigo_frequencia', 'is_active']

class EventoCoordenadorForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['descricao', 'carga_horaria', 'local', 'lotacao', 'site', 'email', 'hora_inicio', 'data_inscricao', 'frequencia_liberada', 'codigo_frequencia']



class BuscaEventoForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    