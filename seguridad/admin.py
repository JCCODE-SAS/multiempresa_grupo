from django.contrib import admin 
from .models import RegistroAcciones, Auditoria
"""
    En este archivo se registran los modelos RegistroAcciones y Auditoria en el panel de administración de Django.
    Se definen los campos a mostrar en la lista, los campos de búsqueda y el ordenamiento de los registros."""

@admin.register(RegistroAcciones)  # Decorador para registrar el modelo en el panel de administración
class RegistroAccionesAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'accion', 'fecha_accion', 'ip_usuario')   # Campos a mostrar en la lista
    search_fields = ('id_usuario__username', 'accion') # Campos de búsqueda
    ordering = ('-fecha_accion',)  # Ordenar por fecha de acción de forma descendente

@admin.register(Auditoria) # Decorador para registrar el modelo en el panel de administración
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'fecha_accion', 'ip_usuario', 'objeto_afectado')   # Campos a mostrar en la lista
    search_fields = ('usuario__username', 'accion', 'objeto_afectado') # Campos de búsqueda
    ordering = ('-fecha_accion',)   # Ordenar por fecha de acción de forma descendente
