from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Anuncio(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio_inicial = models.DecimalField(decimal_places=2, max_digits=10)
    imagen = models.FileField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    categorias = models.ManyToManyField(Categoria)
    publicado_por = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='anuncios_publicados')
    oferta_ganadora = models.OneToOneField('OfertaAnuncio', on_delete=models.SET_NULL,
                                           related_name='oferta_ganadora', blank=True, null=True)

    class Meta:
        ordering = ('fecha_inicio',)

    def __str__(self):
        return f'{self.titulo} - {'Activo' if self.activo else 'Inactivo'} '


class SeguimientoAnuncio(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name='seguimientos')
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='seguimientos_anuncios')

    def __str__(self):
        return f'Anuncio: {self.anuncio.titulo} - Usuario: {self.usuario}'


class OfertaAnuncio(models.Model):
    anuncio = models.ForeignKey('Anuncio', on_delete=models.CASCADE, related_name='ofertas')
    fecha_oferta = models.DateTimeField(auto_now_add=True)
    precio_oferta = models.DecimalField(decimal_places=2, max_digits=10)
    es_ganador = models.BooleanField(default=False)
    usuario = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='ofertas')
