from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf import settings
from . import views as views
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('moderator.urls')),
    path('accounts/', include('allauth.urls')),
]
handler404 = views.error_404
handler500 = views.error_500
if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
