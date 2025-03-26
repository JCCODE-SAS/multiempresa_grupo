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
Configuración de URL para el proyecto Multiempresa.

Este módulo define los patrones de URL del proyecto, mapeando URLs a vistas.
"""
from django.contrib import admin
from django.urls import path, include # Se importa la función include para incluir URLs de otras aplicaciones.
from usuarios import views # se importa correctamente views de la aplicación usuarios


urlpatterns = [
    path('admin/', admin.site.urls), # URL para el panel de administración de Django.
    path('', views.home_view, name='home'),  # Usa la vista home_view
    path('usuarios/', include('usuarios.urls', namespace='usuarios')), # se agrega el namespace 'usuarios' a la aplicación 'usuarios' 
    path('usuarios/login/', views.login_view, name='login'),    # URL para la vista de inicio de sesión.
    
]

