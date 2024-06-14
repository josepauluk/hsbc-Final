from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('cottonLogger.urls')),
    path('', include('post.urls')),
    path('mail/', include('mail.urls')),
    path('error/', include('errorMsg.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'errorMsg.views.error404'
