from django.urls import path
from apps.anuncio import views


app_name = 'anuncio'
urlpatterns = [
    path('', views.lista_anuncios, name='lista_anuncios'),
    path('<int:pk>/', views.detalle_anuncio, name='detalle_anuncio'),
    path('publicar/', views.crear_anuncio, name='crear_anuncio')
]
