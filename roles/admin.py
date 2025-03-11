from django.contrib import admin
from .models import Roles
# Register your models here.
""" este archivo se encarga de registrar el modelo Roles en el panel de administración de Django """
@admin.register(Roles) # Registra el modelo Roles en el panel de administración
class RolesAdmin(admin.ModelAdmin):
    list_display = ('nombre_rol', 'fecha_creacion')  # Muestra estas columnas en el panel 
    search_fields = ('nombre_rol',)  # Permite buscar roles
    ordering = ('fecha_creacion',)  # Ordena por fecha de creación