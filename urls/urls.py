# urls/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shorten/', views.create_short_url, name='create_short_url'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
    path('stats/<str:short_code>/', views.url_stats, name='url_stats'),
]
