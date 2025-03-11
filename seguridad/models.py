from django.db import models 
from usuarios.models import Usuario
"""
Este módulo define los modelos de datos para la aplicación 'seguridad'.
Estos modelos se utilizan para registrar las acciones de los usuarios y
realizar un seguimiento de los cambios importantes dentro del sistema.
"""

class RegistroAcciones(models.Model):
    """
    Representa un registro de las acciones realizadas por los usuarios en el sistema.
    
    """
    id_log = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    accion = models.CharField(max_length=255, blank=True, null=True)
    fecha_accion = models.DateTimeField(auto_now_add=True)  # (DateTimeField): Fecha y hora en que se realizó la acción. Se registra automáticamente la fecha
    ip_usuario = models.GenericIPAddressField(blank=True, null=True)  #Dirección IP del usuario que realizó la acción.  GenericIPAddressField permite Mejor validación de IP

    class Meta: #   Metadatos para el modelo RegistroAcciones; Clase Meta para configurar la tabla en la base de datos
        db_table = 'registro_acciones'  # Nombre de la tabla en la base de datos
        db_table_comment = 'Esta tabla almacena un historial de las acciones realizadas por los usuarios, como accesos y cambios importantes.'
        verbose_name = 'Registro de Acción' # Nombre singular para el modelo en el Admin
        verbose_name_plural = 'Registros de Acciones' # Nombre plural para el modelo en el Admin

class Auditoria(models.Model):
    """
    Representa un registro de auditoría para el seguimiento de cambios en el sistema.
   
    """
    id_log = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, models.SET_NULL, null=True, blank=True, verbose_name="Usuario")
    accion = models.CharField(max_length=255, verbose_name="Acción")
    fecha_accion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Acción")  # Auto-registro de fecha y hora en que se realizó el cambio.

    ip_usuario = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP del Usuario")  # Mejor validación de IP
    objeto_afectado = models.TextField(blank=True, null=True, verbose_name="Objeto Afectado")

    class Meta: # Metadatos para el modelo Auditoria; Clase Meta para configurar la tabla en la base de datos
        db_table = 'auditoria'  # Nombre de la tabla en la base de datos
        verbose_name = 'Registro de Auditoría'  # Nombre singular para el modelo en el Admin
        verbose_name_plural = 'Registros de Auditorías' # Nombre plural para el modelo en el Admin
        ordering = ['-fecha_accion']    # Ordenar los registros por fecha de acción de forma descendente
