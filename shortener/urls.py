# shortener/urls.py

from django.urls import path
# Importa todas as views do seu app
from . import views

# Define os padrões de URL para o app 'shortener'
urlpatterns = [
    # URL para a página inicial (formulário e lista)
    # Mapeia a URL raiz '' para a view index e nomeia como 'index'
    path('', views.index, name='index'),

    # --- Adicionado: URL para a página de status ---
    # Mapeia URLs que começam com 'status/' seguidas por uma string (código curto)
    # para a view status_short_url e nomeia como 'status_short_url'
    # A ordem importa: URLs mais específicas (como 'status/') devem vir antes das menos específicas
    path('status/<str:short_code>/', views.status_short_url, name='status_short_url'),

    # URL para redirecionar o código curto
    # Mapeia qualquer string (código curto) na raiz para a view redirect_short_url
    # e nomeia como 'redirect_short_url'
    path('<str:short_code>/', views.redirect_short_url, name='redirect_short_url'),
]
