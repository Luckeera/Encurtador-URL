# shortener/forms.py - CÓDIGO CORRIGIDO

from django import forms
# Importa o modelo ShortUrl do arquivo models.py
from .models import ShortUrl

# Define o formulário baseado no modelo ShortUrl
class ShortenUrlForm(forms.ModelForm):
    class Meta:
        # Especifica qual modelo este formulário está associado
        model = ShortUrl
        # Define quais campos do modelo serão incluídos no formulário
        fields = ['long_url', 'expires_at']
        widgets = {
            # Opcional: Adicionar um widget de calendário para expires_at
            # Isso requer configuração adicional, como um DatePicker/DateTimePicker
            # Por enquanto, um Input normal funciona, mas o usuário precisa digitar no formato correto
            'expires_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Não há mais a definição da classe ShortUrl(models.Model) aqui!
# Ela reside APENAS em shortener/models.py
