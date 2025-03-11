from django.contrib import admin
from .models import Usuario, IntentosFallidos, Sesiones, CambioContrasena
""" este archivo se encarga de registrar los modelos Usuario, IntentosFallidos, Sesiones y CambioContrasena en el panel de administración de Django """

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'fecha_creacion', 'fecha_ultima_sesion')
    search_fields = ('username', 'email')
    ordering = ('-fecha_creacion',)

@admin.register(IntentosFallidos)
class IntentosFallidosAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'ip_usuario', 'fecha_intento')
    ordering = ('-fecha_intento',)

@admin.register(Sesiones)
class SesionesAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'token_sesion', 'fecha_inicio', 'fecha_fin', 'ip_usuario')
    ordering = ('-fecha_inicio',)

@admin.register(CambioContrasena)
class CambioContrasenaAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'fecha_cambio', 'ip_usuario')
    ordering = ('-fecha_cambio',)
