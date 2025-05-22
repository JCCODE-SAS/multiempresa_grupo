from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre de la Empresa")
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    correo_corporativo = models.EmailField(verbose_name="Correo Electrónico Corporativo")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono Empresarial")
    direccion = models.TextField(verbose_name="Dirección")
    pais = models.CharField(max_length=100, verbose_name="País")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    is_active = models.BooleanField(default=False) # Campo para activar/desactivar la empresa
    usuario_creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa AUTH_USER_MODEL
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empresas_creadas",
        verbose_name="Usuario Creador"
    )
    usuario_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Usa AUTH_USER_MODEL
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="empresas_editadas",
        verbose_name="Último Usuario Editor"
    )

    class Meta:
        db_table = 'empresas'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre