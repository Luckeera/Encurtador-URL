# shortener/models.py

from django.db import models
from django.utils import timezone

class ShortUrl(models.Model):
    long_url = models.URLField(max_length=2000) # Não unique=True mais
    short_code = models.CharField(max_length=10, unique=True) # Código curto deve ser único
    created_at = models.DateTimeField(auto_now_add=True) # Data e hora de criação
    expires_at = models.DateTimeField(null=True, blank=True) # Data e hora de expiração (opcional)
    clicks = models.PositiveIntegerField(default=0) # Campo para contar os cliques

    def __str__(self):
        # Representação em string do objeto, útil no Admin
        return f'{self.short_code} -> {self.long_url}'

    def is_expired(self):
        """Verifica se a URL curta expirou."""
        # Retorna False se expires_at for None (não expira)
        # Retorna True se expires_at for no passado
        if self.expires_at:
            return self.expires_at < timezone.now()
        return False # Não expira se expires_at for None

    class Meta:
        # Ordena os resultados por data de criação por padrão
        ordering = ['-created_at']
