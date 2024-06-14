from django.urls import path
from . import views

urlpatterns = [
    path('403/', views.error403, name='error403'),
    path('404/', views.error404, name='error404'),
]
