# shortener/models.py

from django.db import models
import string
import random
from django.utils import timezone
# from django.conf import settings # Já removemos esta importação

class ShortUrl(models.Model):
    # Remova unique=True daqui
    long_url = models.URLField() # <-- Deve ficar assim agora
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    # O campo user já foi removido no passo anterior
    clicks = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.short_code} -> {self.long_url}'

    def is_expired(self):
        """Verifica se o link expirou."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    def save(self, *args, **kwargs):
        """Gera um short_code único antes de salvar, se não existir."""
        if not self.short_code:
            self.short_code = self._generate_unique_short_code()
        super().save(*args, **kwargs)

    def _generate_unique_short_code(self):
        """Gera um código curto único."""
        length = 6
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            # A verificação de unicidade é apenas para o short_code
            if not ShortUrl.objects.filter(short_code=code).exists():
                return code
