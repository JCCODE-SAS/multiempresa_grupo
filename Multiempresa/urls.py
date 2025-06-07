"""
URL configuration for Multiempresa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for Multiempresa project.
"""
from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuarios_views  # Usa un alias para evitar conflictos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usuarios_views.home_view, name='home'),  # Asegúrate de que esta sea la vista correcta para tu página principal
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('usuarios/login/', usuarios_views.login_view, name='login'),
    path('empresas/', include('empresas.urls', namespace='empresas')),  # Incluye las URLs de la aplicación 'empresas'
    path('admin-empresas/', include('admin_empresas.urls', namespace='admin_empresas')),
    path('roles/', include('roles.urls', namespace='roles')),
]
