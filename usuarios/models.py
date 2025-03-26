from django.db import models
from django.contrib.auth.models import AbstractUser
from roles.models import Roles
import uuid  # Importa la librería uuid
"""
Este módulo define los modelos de datos para la aplicación 'usuarios'.
Estos modelos se utilizan para gestionar la información de los usuarios,
incluyendo datos de perfil, intentos de inicio de sesión fallidos, sesiones activas,
y registros de cambios de contraseña.
"""
class Usuario(AbstractUser):
    """
    Representa un usuario del sistema. Extiende el modelo AbstractUser de Django.  
    
    """
    email = models.EmailField(unique=True)
    rol = models.ForeignKey(Roles, models.SET_NULL, null=True, blank=True, verbose_name="Rol")
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Fecha y hora en que se creó el usuario. Se genera automáticamente.
    fecha_ultima_sesion = models.DateTimeField(blank=True, null=True) # Fecha y hora de la última sesión del usuario.
    token_recuperacion = models.UUIDField(null=True, blank=True, editable=False)  # Token único para recuperación de contraseña.
    is_active = models.BooleanField(default=False)  # Agrega este campo
    USERNAME_FIELD = 'email'  # Campo que se usará para autenticar al usuario.
    REQUIRED_FIELDS = ['username'] # Campos requeridos para crear un usuario.

    class Meta: #  Metadatos para el modelo Usuario; Clase Meta para configurar el modelo.
        db_table = 'usuarios_usuario'   # Nombre de la tabla en la base de datos.
        verbose_name = "Usuario del Sistema"    # Nombre en singular para el modelo en el panel de administración.
        verbose_name_plural = "Usuarios del Sistema" # Nombre en plural para el modelo en el panel de administración.

    def __str__(self):
        return self.username    # Devuelve el nombre de usuario como representación en cadena del objeto.

class IntentosFallidos(models.Model):
    """
    Registra los intentos fallidos de inicio de sesión.
    
    """
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)   # Usuario que intentó iniciar sesión.  
    ip_usuario = models.CharField(max_length=50, blank=True, null=True) # Dirección IP desde la que se intentó iniciar sesión.
    fecha_intento = models.DateTimeField() # Fecha y hora del intento de inicio de sesión.

    class Meta: # Metadatos para el modelo IntentosFallidos.
        db_table = 'intentos_fallidos' # Nombre de la tabla en la base de datos.
        db_table_comment = 'Esta tabla registra los intentos fallidos de login para un usuario específico.' # Comentario de la tabla en la base de datos.
        verbose_name = "Intento Fallido"  # Nombre en singular para el modelo en el panel de administración.
        verbose_name_plural = "Intentos Fallidos" # Nombre en plural para el modelo en el panel de administración.

class Sesiones(models.Model):
    """
    Registra las sesiones activas de los usuarios.
    
    """
    id_sesion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)   # Usuario que inició la sesión.
    token_sesion = models.CharField(max_length=255, blank=True, null=True) # Token de sesión único.
    fecha_inicio = models.DateTimeField() # Fecha y hora de inicio de la sesión.
    fecha_fin = models.DateTimeField(blank=True, null=True) # Fecha y hora de fin de la sesión.
    ip_usuario = models.CharField(max_length=50, blank=True, null=True) # Dirección IP del usuario.
    agente_usuario = models.TextField(blank=True, null=True) # Información del navegador/dispositivo del usuario.

    class Meta: # Metadatos para el modelo Sesiones.
        db_table = 'sesiones'   # Nombre de la tabla en la base de datos.
        db_table_comment = 'Esta tabla almacena las sesiones activas de los usuarios, incluyendo tokens de sesión, IP y agente del usuario.'
        verbose_name = "Sesión" # Nombre en singular para el modelo en el panel de administración.
        verbose_name_plural = "Sesiones" # Nombre en plural para el modelo en el panel de administración.

class CambioContrasena(models.Model):
    
    """
    Registra los cambios de contraseña realizados por los usuarios.
    
    """
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True) # Usuario que cambió la contraseña.
    fecha_cambio = models.DateTimeField() # Fecha y hora del cambio de contraseña.
    ip_usuario = models.CharField(max_length=50, blank=True, null=True) # Dirección IP desde la que se realizó el cambio de contraseña.

    class Meta: # Metadatos para el modelo CambioContrasena.
        db_table = 'cambio_contrasena' # Nombre de la tabla en la base de datos
        db_table_comment = 'Esta tabla registra los cambios de contraseñas realizados por los usuarios.'
        verbose_name = 'Cambio de contraseña'   # Nombre en singular para el modelo en el panel de administración.
        verbose_name_plural = 'Cambios de contraseñas'  # Nombre en plural para el modelo en el panel de administración.
