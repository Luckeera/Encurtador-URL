# shortener/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Rota para a página inicial (criação)
    path('<str:short_code>/', views.redirect_short_url, name='redirect_short_url'), # Rota para o redirecionamento
]
