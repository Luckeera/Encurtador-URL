from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import ShortenedURL
import json

def home(request):
    return render(request, 'urls/home.html')

def create_short_url(request):
    # Criar nova URL encurtada pelo ajax
    if request.method == 'POST':
        try:
            original_url = request.POST.get('original_url')
            
            if not original_url:
                return JsonResponse({'error': 'URL é obrigatória'}, status=400)
            
            # Criar nova URL encurtada
            shortened_url = ShortenedURL.objects.create(
                original_url=original_url,
                created_by=request.user if request.user.is_authenticated else None
            )
            
            # Montar URL completa
            short_url = request.build_absolute_uri(f'/{shortened_url.short_code}/')
            
            return JsonResponse({
                'success': True,
                'short_url': short_url,
                'short_code': shortened_url.short_code,
                'original_url': original_url
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def redirect_url(request, short_code):
    """Redirecionar URL encurtada para original"""
    try:
        # Buscar URL pelo código
        shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
        
        # Verificar se não expirou
        if shortened_url.expires_at and shortened_url.expires_at < timezone.now():
            return render(request, 'urls/expired.html', {'short_code': short_code})
        
        # Verificar se está ativa
        if not shortened_url.is_active:
            return render(request, 'urls/inactive.html', {'short_code': short_code})
        
        # Incrementar contador de cliques
        shortened_url.click_count += 1
        shortened_url.save()
        
        # Redirecionar para URL original
        return redirect(shortened_url.original_url)
        
    except Exception as e:
        return render(request, 'urls/not_found.html', {'short_code': short_code})
