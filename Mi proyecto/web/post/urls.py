from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.galeria, name='post_list'),
    path('upload/', views.MultipleImages, name='upload'),
    path('descargar_fotos_seleccionadas/', views.descargar_fotos_seleccionadas, name='descargar_fotos_seleccionadas'),
    path('descargar_imagen/<int:imagen_id>/', views.descargar_imagen, name='descargar_imagen'),
    path('descargar_todas/', views.descargar_todas, name='descargar_todas'),
    path('eliminar_imagen/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
]