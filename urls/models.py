# urls/models.py
from django.db import models
from django.contrib.auth.models import User
import string
import random
from datetime import datetime

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2048, help_text="URL original para encurtar")
    
    short_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        db_index=True
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shortened_urls'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Deixe vazio para nunca expirar"
    )
    
    click_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.short_code} → {self.original_url[:50]}..."

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        chars = string.ascii_letters + string.digits
        max_attempts = 100
        
        for attempt in range(max_attempts):
            code = ''.join(random.choices(chars, k=6))
            if not ShortenedURL.objects.filter(short_code=code).exists():
                return code
        
        raise Exception("Não conseguiu gerar código único após várias tentativas")

    def is_expired(self):
        if not self.expires_at:
            return False
        return datetime.now() > self.expires_at

    def increment_clicks(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])

    @property
    def display_url(self):
        if len(self.original_url) > 60:
            return self.original_url[:57] + "..."
        return self.original_url

    class Meta:
        ordering = ['-created_at']
        verbose_name = "URL Encurtada"
        verbose_name_plural = "URLs Encurtadas"
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['created_at']),
        ]
