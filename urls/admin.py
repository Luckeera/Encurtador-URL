# urls/admin.py
from django.contrib import admin
from .models import ShortenedURL

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = [
        'short_code', 
        'display_url', 
        'created_by', 
        'click_count', 
        'is_active',
        'created_at'
    ]
    
    list_filter = [
        'is_active', 
        'created_at', 
        'expires_at'
    ]
    
    search_fields = [
        'short_code', 
        'original_url', 
        'created_by__username'
    ]
    
    readonly_fields = [
        'short_code', 
        'created_at', 
        'click_count'
    ]
    
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('URL Information', {
            'fields': ('original_url', 'short_code')
        }),
        ('Settings', {
            'fields': ('is_active', 'expires_at')
        }),
        ('Statistics', {
            'fields': ('click_count', 'created_at'),
            'classes': ('collapse',)
        }),
        ('User', {
            'fields': ('created_by',)
        })
    )

    def display_url(self, obj):
        return obj.display_url
    display_url.short_description = 'URL Original'
