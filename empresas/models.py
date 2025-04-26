from django.db import models

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

    class Meta:
        db_table = 'empresas'
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nombre