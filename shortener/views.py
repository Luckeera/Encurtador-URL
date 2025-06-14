# shortener/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.utils import timezone
from .models import ShortUrl
from .forms import ShortenUrlForm
import string
import random

def generate_short_code(length=6):
    """Gera um código curto alfanumérico único."""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        # Verifica se o código já existe no banco de dados
        if not ShortUrl.objects.filter(short_code=code).exists():
            return code
        # Se existir, tenta gerar outro (evita colisões)

def index(request):
    """View para a página inicial (formulário de criação)."""
    short_url_object = None # Variável para armazenar a URL curta criada, se houver

    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data['long_url']
            expires_at = form.cleaned_data['expires_at']

            # Verifica se a URL longa já existe (opcional, para evitar duplicatas)
            # existing_url = ShortUrl.objects.filter(long_url=long_url, expires_at=expires_at).first()
            # if existing_url:
            #     short_url_object = existing_url # Usa a existente
            # else:
            # Gera um código curto único
            code = generate_short_code()
            # Cria e salva o objeto ShortUrl no banco de dados
            short_url_object = ShortUrl.objects.create(
                long_url=long_url,
                short_code=code,
                expires_at=expires_at
            )

            # Não redirecionamos aqui, apenas mostramos o resultado na mesma página

    else: # request.method == 'GET'
        form = ShortenUrlForm()

    # Renderiza o template, passando o formulário e o objeto ShortUrl (se criado)
    return render(request, 'shortener/index.html', {
        'form': form,
        'short_url_object': short_url_object
    })

def redirect_short_url(request, short_code):
    """View para redirecionar o código curto para a URL longa."""
    # Tenta encontrar o objeto ShortUrl pelo código curto
    url_mapping = get_object_or_404(ShortUrl, short_code=short_code)

    # Verifica se a URL curta expirou
    if url_mapping.is_expired():
        # Se expirou, podemos deletá-la (opcional) e mostrar uma página de erro
        # url_mapping.delete() # Opcional: deletar URLs expiradas ao tentar acessá-las
        return render(request, 'shortener/expired.html', {'short_code': short_code}, status=410) # 410 Gone

    # Se não expirou, redireciona para a URL longa
    return HttpResponseRedirect(url_mapping.long_url)
