from django import forms
from django.db import models

class BuscaFrequenciaForm(forms.Form):        
    pesquisa = forms.CharField(label='Pesquisa livre', required=False)
    
    