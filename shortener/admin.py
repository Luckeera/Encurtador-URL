# shortener/admin.py

from django.contrib import admin
from .models import ShortUrl

# Registra o modelo ShortUrl no site de administração (Primeiro registro)
# admin.site.register(ShortUrl) # <-- Comente ou remova esta linha

# Opcional: Personalizar a exibição no Admin
class ShortUrlAdmin(admin.ModelAdmin): # <-- Mantenha esta classe descomentada
    list_display = ('short_code', 'long_url', 'created_at', 'expires_at', 'is_expired')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('short_code', 'long_url')
    readonly_fields = ('created_at',) # Não permite editar a data de criação

admin.site.register(ShortUrl, ShortUrlAdmin) # <-- Mantenha esta linha descomentada
