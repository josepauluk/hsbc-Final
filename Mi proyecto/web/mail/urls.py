from django.urls import path
from . import views

urlpatterns = [
    path('', views.mail, name='emailSend'),
    path('confirm/', views.sendAll, name='emailSendConfirm'),
]
