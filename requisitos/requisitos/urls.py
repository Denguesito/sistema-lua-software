from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from apps.lua import views as lua_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.lua.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', lua_views.confirmar_logout, name='logout'),
]

# Servir archivos subidos (PDFs) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
