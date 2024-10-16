from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from apps.anuncio.forms import AnuncioForm, AnuncioModificaForm
from apps.anuncio.models import Anuncio
from apps.usuario.models import Usuario


def lista_anuncios(request):
    anuncios = Anuncio.objects.all()
    return render(request, 'anuncio/lista.html', {'anuncios': anuncios})


def detalle_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    return render(request, 'anuncio/detalle.html', {'anuncio': anuncio})


@login_required(login_url='usuario:login')
@permission_required('anuncio.add_anuncio', raise_exception=True)
def crear_anuncio(request):
    nuevo_anuncio = None
    if request.method == 'POST':
        anuncio_form = AnuncioForm(request.POST, request.FILES)
        if anuncio_form.is_valid():
            # Se guardan los datos que provienen del formulario en la B.D.
            nuevo_anuncio = anuncio_form.save(commit=False)
            # crear usuario ficticio
            usuario,_ = Usuario.objects.get_or_create(username='cga', password='321', documento_identidad='63636363')
            nuevo_anuncio.publicado_por = usuario
            nuevo_anuncio.save()
            # Esto guarda específicamente las relaciones ManyToMany (como el campo categorias)
            # después de que el objeto principal ha sido guardado.
            anuncio_form.save_m2m()
            messages.success(request,
                             'Se ha agregado correctamente el Anuncio {}'.format(nuevo_anuncio))
            return redirect(reverse('anuncio:detalle_anuncio', args={nuevo_anuncio.id}))
    else:
        anuncio_form = AnuncioForm()

    return render(request, 'anuncio/anuncio_form.html', {'form': anuncio_form})


@permission_required('anuncio.change_anuncio', raise_exception=True)
def editar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)

    # verificar que el usuario que desea modificar el anuncio, sea quien creó la publicación
    if not anuncio.publicado_por == request.user:
        messages.error(request, 'Ud no puede modificar el Anuncio')
        return redirect(reverse('anuncio:detalle_anuncio', args=[anuncio.id]))

    if request.method == 'POST':
        form_anuncio = AnuncioModificaForm(request.POST, request.FILES, instance=anuncio)
        if form_anuncio.is_valid():
            form_anuncio.save(commit=True)
            messages.success(request, 'Se ha actualizado correctamente el Anuncio')
            return redirect(reverse('anuncio:detalle_anuncio', args=[anuncio.id]))
    else:
        form_anuncio = AnuncioModificaForm(instance=anuncio)

    return render(request, 'anuncio/anuncio_form.html', {'form': form_anuncio})


@permission_required('anuncio.delete_anuncio', raise_exception=True)
def eliminar_anuncio(request):
    if request.method == 'POST':
        if 'id_anuncio' in request.POST:
            anuncio = get_object_or_404(Anuncio, pk=request.POST['id_anuncio'])

            # verificar que el usuario que desea modificar el anuncio, sea quien creó la publicación
            if not anuncio.publicado_por == request.user:
                messages.error(request, 'Ud no puede eliminar el Anuncio')
                return redirect(reverse('anuncio:detalle_anuncio', args=[anuncio.id]))

            titulo_anuncio = anuncio.titulo
            anuncio.delete()
            messages.success(request, 'Se ha eliminado exitosamente el Anuncio {}'.format(titulo_anuncio))
        else:
            messages.error(request, 'Debe indicar qué Anuncio se desea eliminar')
    return redirect(reverse('anuncio:lista_anuncios'))
