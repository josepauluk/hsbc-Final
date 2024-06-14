from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.http import HttpResponse
import io
import zipfile
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework import serializers
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.models import User
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from rest_framework.response import Response


# SECCION API
# @login_required
class GaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'imagen')


# @login_required
@api_view(['GET'])
def galeria(request):
    if not request.user.is_authenticated:
        return redirect('logger_main')
    posts = Post.objects.all()
    paginator = Paginator(posts, 24) # Muestra 24 resultados por página
    page = request.GET.get('page')
    cant_imagenes = posts.count()

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'page': page,
        'cant_imagenes':cant_imagenes,
    }
    return render(request, 'post/post_list.html', context)

#FIN SECCION API


# def es_superusuario(user):
#     return user.is_superuser
# @login_required
# def post_list(request):
#     if not request.user.is_authenticated:
#         return redirect('error404')
#     posts = Post.objects.all()
#     return render(request, 'post/post_list.html', {'posts': posts})
# 
#     cant_imagenes = posts.count()
#     return render(request, 'post/post_list.html', {'posts': posts , 'cant_imagenes':cant_imagenes,})


def MultipleImages(request):
    if not request.user.is_superuser:
        return redirect('error404')
    if request.method == "POST":
        fotos = request.FILES.getlist('images')
        if len(fotos)>100:
            messages.error(request,'No puede subir más de 100 imágenes por vez')
            return render(request, "post/upload.html")
        for foto in fotos:
            Post.objects.create(foto=foto)
            
        messages.success(request, 'Imágenes subidas correctamente.')
        
        return HttpResponseRedirect(reverse_lazy('post_list'))
    return render(request, "post/upload.html")


def eliminar_imagen(request, imagen_id):
    if not request.user.is_superuser:
        return redirect('error404')
    imagen = get_object_or_404(Post, id=imagen_id)
    
    # Eliminar el archivo del sistema de archivos
    if os.path.isfile(imagen.foto.path):
        os.remove(imagen.foto.path)
    
    imagen.delete()
    messages.success(request, 'Imagen eliminada correctamente.')
    return HttpResponseRedirect(reverse_lazy('post_list'))


def descargar_imagen(request, imagen_id):
    if not request.user.is_authenticated:
        return redirect('error404')
    # Busca la imagen por ID
    imagen = get_object_or_404(Post, id=imagen_id)

    # Devuelve la imagen como archivo para descargar
    response = FileResponse(open(imagen.foto.path, 'rb'),
                            as_attachment=True, filename=imagen.foto.url)
    return response


def descargar_fotos_seleccionadas(request):
    if not request.user.is_authenticated:
        return redirect('error404')
    if request.method == 'POST':
        # Obteniene los IDs de las imágenes seleccionadas
        imagenes_descarga = request.POST.getlist('imagenes_descarga[]')
    
        if imagenes_descarga == []:
            
            return HttpResponseRedirect(reverse_lazy('post_list'))
        else:
            # Crea un archivo ZIP en memoria
            memoria_zip = io.BytesIO()

            # Crea un objeto ZipFile y agrega las imágenes seleccionadas
            with zipfile.ZipFile(memoria_zip, mode='w') as archivo_zip:
                for imagen_id in imagenes_descarga:
                    imagen = Post.objects.get(pk=imagen_id)
                    archivo_zip.write(imagen.foto.path, imagen.foto.url)

            # Devuelve el archivo ZIP como una respuesta de descarga
            response = HttpResponse(
                memoria_zip.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="imagenes.zip"'
            return response

    # Si el método de solicitud no es POST, redirige a la galaria
    return HttpResponseRedirect(reverse_lazy('post_list'))


def descargar_todas(request):
    if not request.user.is_authenticated:
        return redirect('error404')
    imagenes = Post.objects.all()
    # Crea un archivo ZIP en memoria para guardar las imágenes
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Agrega cada imagen al archivo ZIP
        for imagen in imagenes:
            zip_file.write(imagen.foto.path, imagen.foto.url)

    # Envía el archivo ZIP como respuesta para su descarga
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="Fotos_del_evento.zip"'
    return response

