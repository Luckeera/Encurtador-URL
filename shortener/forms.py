# shortener/forms.py

from django import forms

class ShortenUrlForm(forms.Form):
    long_url = forms.URLField(
        label="URL Longa",
        max_length=500,
        widget=forms.URLInput(attrs={'placeholder': 'Cole sua URL longa aqui'})
    )
    expires_at = forms.DateTimeField(
        label="Expira em (Opcional)",
        required=False, # Torna o campo opcional
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), # Widget HTML5 para data/hora
        input_formats=['%Y-%m-%dT%H:%M'], # Formato esperado do widget datetime-local
        help_text="Deixe em branco para nunca expirar."
    )
