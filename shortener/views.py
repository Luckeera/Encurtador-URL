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
    """View para a página inicial (formulário de criação e lista de URLs)."""
    short_url_object = None # Variável para armazenar a URL curta criada, se houver

    if request.method == 'POST':
        form = ShortenUrlForm(request.POST)
        if form.is_valid():
            long_url = form.cleaned_data['long_url']
            expires_at = form.cleaned_data['expires_at']

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

    # --- Adicionado: Busca todos os objetos ShortUrl para exibir na lista ---
    # O .all() busca todos os registros da tabela ShortUrl
    # A ordenação padrão é definida no Meta do modelo (-created_at)
    all_urls = ShortUrl.objects.all()

    # Renderiza o template, passando o formulário, o objeto ShortUrl (se criado) e a lista de todas as URLs
    return render(request, 'shortener/index.html', {
        'form': form,
        'short_url_object': short_url_object, # Objeto da URL criada na submissão POST (pode ser None em GET)
        'all_urls': all_urls, # Lista de todas as URLs para exibir
    })

def redirect_short_url(request, short_code):
    """View para redirecionar o código curto para a URL longa e contar cliques."""
    # Tenta encontrar o objeto ShortUrl pelo código curto
    # get_object_or_404 retorna o objeto ou um erro 404 se não encontrar
    url_mapping = get_object_or_404(ShortUrl, short_code=short_code)

    # Verifica se a URL curta expirou usando o método do modelo
    if url_mapping.is_expired():
        # Se expirou, renderiza uma página de erro 410 Gone (Removido Permanentemente)
        # Opcional: url_mapping.delete() # Descomente para deletar URLs expiradas ao acessar
        return render(request, 'shortener/expired.html', {'short_code': short_code}, status=410)

    # --- Adicionado: Incrementa o contador de cliques ---
    url_mapping.clicks += 1 # Soma 1 ao campo clicks
    url_mapping.save()   # Salva a alteração no banco de dados

    # Se não expirou, redireciona para a URL longa
    return HttpResponseRedirect(url_mapping.long_url)

# --- Nova View: Página de Status da URL ---
def status_short_url(request, short_code):
    """View para exibir a página de status de uma URL curta."""
    # Tenta encontrar o objeto ShortUrl pelo código curto
    # get_object_or_404 retorna o objeto ou um erro 404 se não encontrar
    url_object = get_object_or_404(ShortUrl, short_code=short_code)

    # Renderiza o template de status, passando o objeto ShortUrl encontrado
    return render(request, 'shortener/status.html', {
        'short_url_object': url_object, # Objeto da URL para exibir os detalhes
    })
