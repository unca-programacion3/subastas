from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from apps.anuncio.forms import AnuncioForm, AnuncioModificaForm
from apps.anuncio.models import Anuncio


def lista_anuncios(request):
    anuncios = Anuncio.objects.all()
    return render(request, 'anuncio/lista.html', {'anuncios': anuncios})


def detalle_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    return render(request, 'anuncio/detalle.html', {'anuncio': anuncio})


def crear_anuncio(request):
    nuevo_anuncio = None
    if request.method == 'POST':
        anuncio_form = AnuncioForm(request.POST, request.FILES)
        if anuncio_form.is_valid():
            # Se guardan los datos que provienen del formulario en la B.D.
            nuevo_anuncio = anuncio_form.save(commit=False)
            nuevo_anuncio.publicado_por = request.user
            nuevo_anuncio.save()
            messages.success(request,
                             'Se ha agregado correctamente el Anuncio {}'.format(nuevo_anuncio))
            return redirect(reverse('anuncio:detalle_anuncio', args={nuevo_anuncio.id}))
    else:
        anuncio_form = AnuncioForm()

    return render(request, 'anuncio/anuncio_form.html', {'form': anuncio_form})


def editar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if request.method == 'POST':
        form_anuncio = AnuncioModificaForm(request.POST, request.FILES, instance=anuncio)
        if form_anuncio.is_valid():
            form_anuncio.save(commit=True)
            messages.success(request, 'Se ha actualizado correctamente el Anuncio')
            return redirect(reverse('anuncio:detalle_anuncio', args=[anuncio.id]))
    else:
        form_anuncio = AnuncioModificaForm(instance=anuncio)

    return render(request, 'anuncio/anuncio_form.html', {'form': form_anuncio})
