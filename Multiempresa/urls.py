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
from django.shortcuts import redirect # Se importa la función redirect para redirigir a una URL.
from usuarios import views # se importa correctamente views de la aplicación usuarios

def home_redirect(request): # Función para redirigir a la vista de inicio de sesión.    
    return redirect('/usuarios/login/') # Redirige a la vista de inicio de sesión.

urlpatterns = [
    path('admin/', admin.site.urls), # URL para el panel de administración de Django.
    path('', home_redirect, name='home'), # URL para redirigir a la página de inicio.
    path('usuarios/', include('usuarios.urls', namespace='usuarios')), # se agrega el namespace 'usuarios' a la aplicación 'usuarios' 
    path('usuarios/login/', views.login_view, name='login'),    # URL para la vista de inicio de sesión.
    
]

